import json
import os
from enum import Enum
from typing import Any, Optional

import httpx
from pydantic import BaseModel, field_validator

from util import env_var


class DeviceCapability(str, Enum):
    """Enum of supported Hubitat device capabilities."""

    SWITCH = "Switch"
    SWITCH_LEVEL = "SwitchLevel"
    MOTION_SENSOR = "MotionSensor"
    CONTACT_SENSOR = "ContactSensor"
    PRESENCE_SENSOR = "PresenceSensor"
    TEMPERATURE_MEASUREMENT = "TemperatureMeasurement"
    RELATIVE_HUMIDITY_MEASUREMENT = "RelativeHumidityMeasurement"
    GARAGE_DOOR_CONTROL = "GarageDoorControl"

    @classmethod
    def allowed_capabilities(cls) -> list[str]:
        """Return a list of all allowed capability values."""
        return [capability.value for capability in cls]


class DeviceAttribute(BaseModel):
    """Represents a device attribute with its properties and restrictions."""

    name: str
    value_type: str
    restrictions: Optional[dict[str, Any]] = None
    special_info: Optional[str] = None

    def __hash__(self):
        return hash(self.name)


class CommandArgument(BaseModel):
    """Represents an argument for a device command."""

    name: str
    value_type: str
    restrictions: dict[str, Any] = {}
    required: bool = False

    def __hash__(self):
        return hash(self.name)


class DeviceCommand(BaseModel):
    """Represents a command that can be sent to a device."""

    name: str
    arguments: Optional[list[CommandArgument]] = None

    def __hash__(self):
        return hash(self.name)


def _load_json_file(filename: str) -> dict[str, Any]:
    """Load a JSON file from the current directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    with open(file_path, "r") as f:
        return json.load(f)


def _load_attributes() -> dict[DeviceCapability, list[DeviceAttribute]]:
    """Load device attributes from JSON and convert to the appropriate types."""
    json_data = _load_json_file("capability_attributes.json")
    result: dict[DeviceCapability, list[DeviceAttribute]] = {}

    for cap_str, attributes in json_data.items():
        # Convert string to enum
        capability = DeviceCapability(cap_str)
        # Convert dict to DeviceAttribute objects
        attr_objects = [DeviceAttribute(**attr) for attr in attributes]
        result[capability] = attr_objects

    return result


def _load_commands() -> dict[DeviceCapability, list[DeviceCommand]]:
    """Load device commands from JSON and convert to the appropriate types."""
    json_data = _load_json_file("capability_commands.json")
    result: dict[DeviceCapability, list[DeviceCommand]] = {}

    for cap_str, commands in json_data.items():
        # Convert string to enum
        capability = DeviceCapability(cap_str)

        # Convert dict to DeviceCommand objects
        cmd_objects = []
        for cmd in commands:
            # Handle arguments if present
            if "arguments" in cmd:
                # Convert dict to CommandArgument objects
                args = [CommandArgument(**arg) for arg in cmd["arguments"]]
                cmd_obj = DeviceCommand(name=cmd["name"], arguments=args)
            else:
                cmd_obj = DeviceCommand(name=cmd["name"])
            cmd_objects.append(cmd_obj)

        result[capability] = cmd_objects

    return result


# Load dictionaries from JSON files
capability_attributes: dict[DeviceCapability, list[DeviceAttribute]] = (
    _load_attributes()
)
capability_commands: dict[DeviceCapability, list[DeviceCommand]] = _load_commands()


class HubitatDevice(BaseModel):
    """Represents a Hubitat device with its capabilities and attributes."""

    id: int
    label: str
    room: str
    capabilities: list[str]
    attributes: set[DeviceAttribute]
    commands: set[DeviceCommand]

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any) -> int:
        """Validate and convert device ID to integer."""
        if isinstance(v, int):
            return v
        if isinstance(v, str) and v.isdigit():
            return int(v)
        raise ValueError(f"Device ID must be a valid integer, got {v!r}")

    def attribute_by_name(self, name: str) -> DeviceAttribute | None:
        """Get an attribute by name."""
        for attr in self.attributes:
            if attr.name == name:
                return attr
        return None

    def command_by_name(self, name: str) -> DeviceCommand | None:
        """Get a command by name."""
        for cmd in self.commands:
            if cmd.name == name:
                return cmd
        return None


class HubitatClient:
    """Wrapper around Hubitat functionalities."""

    def __init__(self):
        """Initialize the Hubitat client with connection details."""
        self._address = (
            f"http://{env_var('HE_ADDRESS')}/apps/api/{env_var('HE_APP_ID')}"
        )
        self._token = env_var("HE_ACCESS_TOKEN")

    async def send_command(
        self, device_id: int, command: str, arguments: Optional[list[Any]] = None
    ):
        """Send a command with optional arguments to a device.

        Args:
            device_id: The ID of the device to send the command to
            command: The command to send
            arguments: Optional list of arguments for the command
        """
        url = f"{self._address}/devices/{device_id}/{command}"
        if arguments:
            url += f"/{','.join(str(arg) for arg in arguments)}"

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, params={"access_token": self._token})
            except httpx.HTTPStatusError as error:
                raise Exception(
                    f"HE Client returned '{error.response.status_code}' "
                    f"status: {error.response.text}"
                ) from error
            except Exception as error:
                print(f"HE Client returned error: {error}")
                raise

        if resp.status_code != 200:
            raise Exception(
                f"HE Client returned '{resp.status_code}' status: {resp.text}"
            )

    async def get_attribute(self, device_id: int, attribute: str) -> Any:
        """Get the current value of a device attribute.

        Args:
            device_id: The ID of the device to get the attribute from
            attribute: The name of the attribute to get

        Returns:
            The current value of the attribute, or None if not found
        """
        url = f"{self._address}/devices/{device_id}"

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, params={"access_token": self._token})
            except httpx.HTTPStatusError as error:
                raise Exception(
                    f"HE Client returned '{error.response.status_code}' "
                    f"status: {error.response.text}"
                ) from error
            except Exception as error:
                print(f"HE Client returned error: {error}")
                raise

        if resp.status_code != 200:
            raise Exception(
                f"HE Client returned '{resp.status_code}' status: {resp.text}"
            )

        attributes: list[dict[str, Any]] = resp.json()["attributes"]
        for attr in attributes:
            if attr["name"] == attribute:
                return attr["currentValue"]

        return None
