"""Hubitat device models."""

from typing import Any
from pydantic import BaseModel, field_validator

from .capabilities import DeviceAttribute, DeviceCommand


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
