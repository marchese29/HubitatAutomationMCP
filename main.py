"""FastMCP server implementation for Hubitat capabilities."""

import asyncio
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from fastmcp.resources import TextResource

from hubitat import HubitatClient
from models.capabilities import DeviceCapability
from models.devices import (
    CommandExecutionResult,
    CommandRequest,
    DeviceStateInfo,
    HubitatDeviceInfo,
)
from room_manager import RoomManager


# Initialize FastMCP server
mcp = FastMCP("Hubitat Capabilities")

# Initialize shared resources
he_client = HubitatClient()
room_manager = RoomManager(he_client)

script_dir = Path(__file__).parent


@mcp.tool(
    name="get_capability_attributes",
    description="The available device attributes for each device capability"
)
async def get_capability_attributes() -> str:
    attributes_path = script_dir / "capability_attributes.json"
    with open(attributes_path, "r") as f:
        return f.read()


@mcp.tool(
    name="get_capability_commands",
    description="The available commands for each device capability"
)
async def get_capability_commands() -> str:
    commands_path = script_dir / "capability_commands.json"
    with open(commands_path, "r") as f:
        return f.read()


# @mcp.resource("hubitat://layout", name="Home Layout")
@mcp.tool()
async def get_room_layout() -> str:
    """Get the current room hierarchy and device assignments.

    Dynamically loads the rooms.json file each time to ensure
    up-to-date room structure is returned.

    Returns:
        JSON string containing current room hierarchy and device assignments
    """
    rooms_path = script_dir / "rooms.json"
    try:
        with open(rooms_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        # Return empty room structure if file doesn't exist yet
        return '{"rooms": {}, "adjacency": {}}'


# @mcp.resource("hubitat://capabilities", name="Capabilities")
@mcp.tool()
async def get_all_capabilities() -> dict[str, Any]:
    """Get a list of all available Hubitat capabilities.

    Returns:
        JSON string containing an array of capability names
    """
    capabilities = DeviceCapability.allowed_capabilities()
    return {"capabilities": capabilities, "count": len(capabilities)}


@mcp.resource("hubitat://devices", name="Current Devices")
async def get_all_devices() -> list[HubitatDeviceInfo]:
    """Get all devices from Hubitat without attributes and commands.

    Provides device discovery by returning basic device information including
    ID, name, label, type, capabilities, etc. but excluding current attribute
    values and available commands (which can be looked up via capabilities).

    Returns:
        List of HubitatDeviceInfo objects with device metadata
    """

    return [
        HubitatDeviceInfo.from_hubitat_device(device)
        for device in await he_client.get_all_devices()
    ]


# Helper function for safe command execution
async def _execute_command_safely(cmd: CommandRequest) -> CommandExecutionResult:
    """Execute a single command with error handling."""

    try:
        await he_client.send_command(cmd.device_id, cmd.command, cmd.arguments)
        return CommandExecutionResult(
            device_id=cmd.device_id,
            command=cmd.command,
            arguments=cmd.arguments,
            success=True,
        )
    except Exception as e:
        return CommandExecutionResult(
            device_id=cmd.device_id,
            command=cmd.command,
            arguments=cmd.arguments,
            success=False,
            error_message=str(e),
        )


@mcp.tool()
async def get_device_states(device_ids: list[int]) -> list[DeviceStateInfo]:
    """Get current state of specified devices.

    Uses the /devices/all endpoint to fetch device information and filters
    by the requested device IDs, returning only the current attribute values.

    Args:
        device_ids: List of device IDs to retrieve states for

    Returns:
        List of DeviceStateInfo objects with device information and current attribute values
    """
    all_devices = await he_client.get_all_devices()

    # Filter devices by requested IDs and convert using class method
    requested_devices = []
    for device in all_devices:
        device_id = int(device.id)  # Convert string ID to int
        if device_id in device_ids:
            device_info = DeviceStateInfo.from_hubitat_device(device)
            requested_devices.append(device_info)

    return requested_devices


@mcp.tool()
async def send_commands(commands: list[CommandRequest]) -> list[CommandExecutionResult]:
    """Send multiple commands to devices in parallel.

    Executes all commands concurrently and returns success/failure status
    for each command. Failed commands do not stop execution of other commands.

    Args:
        commands: List of commands to execute

    Returns:
        List of CommandExecutionResult objects with results for each command
    """
    return await asyncio.gather(
        *[_execute_command_safely(cmd) for cmd in commands],
        return_exceptions=False,  # We handle exceptions in execute_command_safely
    )


# Room Management Tools


@mcp.tool()
async def create_room(
    name: str,
    device_ids: list[int],
    description: str | None = None,
    notes: str | None = None,
) -> dict:
    """Create a new room with specified devices.

    Args:
        name: Unique name for the room
        device_ids: List of Hubitat device IDs to assign to this room
        description: Optional room description
        notes: Optional special notes about the room

    Returns:
        Dict with success status and message or error details
    """
    return await room_manager.create_room(name, device_ids, description, notes)


@mcp.tool()
async def get_devices_in_room(name: str) -> list[DeviceStateInfo]:
    """Get full device state information for all devices in a room and its child rooms.

    Recursively collects devices from the specified room and all of its child rooms
    in the hierarchy, returning deduplicated device state information.

    Args:
        name: Name of the room to get devices for

    Returns:
        List of DeviceStateInfo objects with current attribute values from the room
        and all its child rooms (deduplicated)
    """
    return await room_manager.get_devices_in_room(name)


@mcp.tool()
async def add_devices_to_room(name: str, device_ids: list[int]) -> dict:
    """Add devices to an existing room's device list.

    Args:
        name: Name of the room to add devices to
        device_ids: List of Hubitat device IDs to add

    Returns:
        Dict with success status, message, and total device count
    """
    return await room_manager.add_devices_to_room(name, device_ids)


@mcp.tool()
async def add_room_relationships(parent_name: str, child_names: list[str]) -> dict:
    """Create parent→children relationships in the room hierarchy.

    Args:
        parent_name: Name of the parent room
        child_names: List of child room names to add as children

    Returns:
        Dict with success status and message or cycle detection error
    """
    return await room_manager.add_room_relationships(parent_name, child_names)


@mcp.tool()
async def delete_rooms(names: list[str]) -> dict:
    """Remove rooms and all their relationships from the system.

    Args:
        names: List of room names to delete

    Returns:
        Dict with deleted rooms list and any missing rooms
    """
    return await room_manager.delete_rooms(names)


if __name__ == "__main__":
    mcp.run()
