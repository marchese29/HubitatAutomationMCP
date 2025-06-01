"""Room management system with JSON-based DAG storage."""

import json
import tempfile
from pathlib import Path
from typing import Optional

from hubitat import HubitatClient
from models.devices import DeviceStateInfo
from models.rooms import Room, RoomData


class RoomManager:
    """Manages room data persistence and validation."""

    def __init__(self, he_client: HubitatClient, file_path: Path = Path("rooms.json")):
        """Initialize room manager with JSON file path."""
        self._he_client = he_client
        self._file_path = file_path

    async def load_rooms(self) -> RoomData:
        """Load room data from JSON file, creating empty structure if missing."""
        try:
            if not self._file_path.exists():
                return RoomData()

            with open(self._file_path, "r") as f:
                data = json.load(f)

            return RoomData(**data)
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            # If file is corrupted or malformed, return empty structure
            return RoomData()

    async def save_rooms(self, data: RoomData) -> None:
        """Atomically save room data to JSON file with backup."""
        # Create a temporary file for atomic write
        with tempfile.NamedTemporaryFile(
            mode="w", dir=self._file_path.parent, delete=False, suffix=".tmp"
        ) as tmp_file:
            json.dump(data.model_dump(), tmp_file, indent=2)
            tmp_path = Path(tmp_file.name)

        # Atomic rename to replace the original file
        tmp_path.replace(self._file_path)

    def detect_cycle(
        self, parent: str, children: list[str], adjacency: dict[str, list[str]]
    ) -> bool:
        """Check if adding parent->children relationships would create cycles."""
        for child in children:
            if self._path_exists(child, parent, adjacency):
                return True
        return False

    def _path_exists(
        self, start: str, target: str, adjacency: dict[str, list[str]]
    ) -> bool:
        """DFS to check if path exists from start to target."""
        visited = set()
        stack = [start]

        while stack:
            current = stack.pop()
            if current == target:
                return True
            if current in visited:
                continue
            visited.add(current)
            stack.extend(adjacency.get(current, []))

        return False

    async def validate_devices_exist(self, device_ids: list[int]) -> bool:
        """Validate device IDs exist in Hubitat using existing client."""
        try:
            all_devices = await self._he_client.get_all_devices()
            existing_ids = {int(device.id) for device in all_devices}
            return all(device_id in existing_ids for device_id in device_ids)
        except Exception:
            # If we can't validate, assume devices don't exist for safety
            return False

    def remove_room_from_adjacency(
        self, room_name: str, adjacency: dict[str, list[str]]
    ) -> None:
        """Remove all references to room from adjacency structure."""
        # Remove as parent
        if room_name in adjacency:
            del adjacency[room_name]

        # Remove as child from all parents
        for parent, children in adjacency.items():
            if room_name in children:
                children.remove(room_name)

    async def create_room(
        self,
        name: str,
        device_ids: list[int],
        description: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> dict:
        """Create a new room with specified devices."""
        data = await self.load_rooms()

        # Check if room already exists
        if name in data.rooms:
            return {"success": False, "error": f"Room '{name}' already exists"}

        # Validate device IDs exist
        if device_ids and not await self.validate_devices_exist(device_ids):
            return {
                "success": False,
                "error": "One or more device IDs do not exist in Hubitat",
            }

        # Create new room
        data.rooms[name] = Room(
            device_ids=device_ids, description=description, notes=notes
        )

        await self.save_rooms(data)
        return {"success": True, "message": f"Room '{name}' created successfully"}

    def get_all_child_rooms(
        self, room_name: str, adjacency: dict[str, list[str]]
    ) -> set[str]:
        """Recursively get all child room names for a given room."""
        all_children = set()

        def collect_children(current_room: str):
            children = adjacency.get(current_room, [])
            for child in children:
                if child not in all_children:  # Prevent infinite loops
                    all_children.add(child)
                    collect_children(child)

        collect_children(room_name)
        return all_children

    async def get_devices_in_room(self, name: str) -> list[DeviceStateInfo]:
        """Get full device state information for room's devices and all child room devices."""
        data = await self.load_rooms()

        if name not in data.rooms:
            return []

        # Collect device IDs from the room and all its children
        all_device_ids = set()

        # Add devices from the target room
        room = data.rooms[name]
        all_device_ids.update(room.device_ids)

        # Add devices from all child rooms recursively
        child_rooms = self.get_all_child_rooms(name, data.adjacency)
        for child_room in child_rooms:
            if child_room in data.rooms:
                child_room_obj = data.rooms[child_room]
                all_device_ids.update(child_room_obj.device_ids)

        if not all_device_ids:
            return []

        # Use existing HubitatClient to get device states
        try:
            all_devices = await self._he_client.get_all_devices()

            # Filter devices by collected device IDs and convert
            requested_devices = []
            for device in all_devices:
                device_id = int(device.id)
                if device_id in all_device_ids:
                    device_info = DeviceStateInfo.from_hubitat_device(device)
                    requested_devices.append(device_info)

            return requested_devices
        except Exception:
            return []

    async def add_devices_to_room(self, name: str, device_ids: list[int]) -> dict:
        """Add devices to existing room's device list."""
        data = await self.load_rooms()

        if name not in data.rooms:
            return {"success": False, "error": f"Room '{name}' does not exist"}

        # Validate device IDs exist
        if not await self.validate_devices_exist(device_ids):
            return {
                "success": False,
                "error": "One or more device IDs do not exist in Hubitat",
            }

        room = data.rooms[name]
        # Add new devices, avoiding duplicates
        original_count = len(room.device_ids)
        room.device_ids = list(set(room.device_ids + device_ids))
        new_count = len(room.device_ids)

        await self.save_rooms(data)
        added_count = new_count - original_count
        return {
            "success": True,
            "message": f"Added {added_count} devices to room '{name}'",
            "total_devices": new_count,
        }

    async def add_room_relationships(
        self, parent_name: str, child_names: list[str]
    ) -> dict:
        """Create parent→children relationships in adjacency structure."""
        data = await self.load_rooms()

        # Validate all rooms exist
        all_room_names = set(data.rooms.keys())
        if parent_name not in all_room_names:
            return {
                "success": False,
                "error": f"Parent room '{parent_name}' does not exist",
            }

        missing_children = [name for name in child_names if name not in all_room_names]
        if missing_children:
            return {
                "success": False,
                "error": f"Child rooms do not exist: {missing_children}",
            }

        # Check for cycles
        if self.detect_cycle(parent_name, child_names, data.adjacency):
            return {
                "success": False,
                "error": "Adding relationship would create cycle",
            }

        # Add relationships
        if parent_name not in data.adjacency:
            data.adjacency[parent_name] = []

        # Add new children, avoiding duplicates
        original_children = set(data.adjacency[parent_name])
        new_children = set(child_names)
        data.adjacency[parent_name] = list(original_children | new_children)

        await self.save_rooms(data)
        added_count = len(new_children - original_children)
        return {
            "success": True,
            "message": f"Added {added_count} child relationships to '{parent_name}'",
        }

    async def delete_rooms(self, names: list[str]) -> dict:
        """Remove rooms and all their relationships."""
        data = await self.load_rooms()

        existing_rooms = [name for name in names if name in data.rooms]
        missing_rooms = [name for name in names if name not in data.rooms]

        # Remove rooms and their adjacency references
        for room_name in existing_rooms:
            del data.rooms[room_name]
            self.remove_room_from_adjacency(room_name, data.adjacency)

        await self.save_rooms(data)

        result = {"success": True, "deleted_rooms": existing_rooms}
        if missing_rooms:
            result["missing_rooms"] = missing_rooms

        return result
