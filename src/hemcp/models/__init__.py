"""Shared models for Hubitat automation and MCP server."""

from .capabilities import (
    DeviceCapability,
    DeviceAttribute,
    CommandArgument,
    DeviceCommand,
    load_attributes,
    load_commands,
)
from .devices import HubitatDevice

__all__ = [
    "DeviceCapability",
    "DeviceAttribute",
    "CommandArgument",
    "DeviceCommand",
    "load_attributes",
    "load_commands",
    "HubitatDevice",
]
