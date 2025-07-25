"""Hubitat device models."""

from typing import Any, Self
from pydantic import BaseModel, field_validator

from ..models.capabilities import DeviceAttribute, DeviceCommand


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


class HubitatDeviceResponse(BaseModel):
    """Full device response from /devices/all endpoint."""

    id: str  # Hubitat returns this as string
    name: str
    label: str
    type: str
    date: str | None = None  # API can return None for date
    model: str | None = None
    manufacturer: str | None = None
    capabilities: list[str]
    attributes: dict[str, Any] | None = None
    commands: list[dict[str, str]] | None = None


class DeviceStateInfo(BaseModel):
    """Individual device state information."""

    id: int
    name: str
    label: str
    type: str
    attributes: dict[str, Any]  # Current attribute values only

    @classmethod
    def from_hubitat_device(cls, device: HubitatDeviceResponse) -> Self:
        """Create a DeviceStateInfo from a HubitatDeviceResponse."""
        return cls(
            id=int(device.id),  # Convert string ID to int
            name=device.name,
            label=device.label,
            type=device.type,
            attributes=device.attributes or {},  # Handle None case
        )


class HubitatDeviceInfo(BaseModel):
    """Device information without attributes and commands."""

    id: int
    name: str
    label: str
    type: str
    date: str | None = None
    model: str | None = None
    manufacturer: str | None = None
    capabilities: list[str]

    @classmethod
    def from_hubitat_device(cls, device: HubitatDeviceResponse) -> Self:
        """Create a HubitatDeviceInfo from a HubitatDeviceResponse."""
        return cls(
            id=int(device.id),
            name=device.name,
            label=device.label,
            type=device.type,
            date=device.date,
            model=device.model,
            manufacturer=device.manufacturer,
            capabilities=device.capabilities,
        )


class CommandRequest(BaseModel):
    """Individual command to execute."""

    device_id: int
    command: str
    arguments: list[Any] | None = None


class CommandExecutionResult(BaseModel):
    """Result of a single command execution."""

    device_id: int
    command: str
    arguments: list[Any] | None = None
    success: bool
    error_message: str | None = None
