"""FastMCP server implementation for Hubitat capabilities."""

from typing import Any

from fastmcp import FastMCP

from hubitat_mcp.data_loader import CapabilityDataLoader
from models.capabilities import DeviceAttribute, DeviceCommand


# Initialize FastMCP server
mcp = FastMCP("Hubitat Capabilities")


@mcp.resource("hubitat://capabilities")
async def get_all_capabilities() -> dict[str, Any]:
    """Get a list of all available Hubitat capabilities.

    Returns:
        JSON string containing an array of capability names
    """
    capabilities = CapabilityDataLoader.get_all_capability_names()
    return {"capabilities": capabilities, "count": len(capabilities)}


@mcp.resource("hubitat://capabilities/{capability_name}/attributes")
async def get_capability_attributes(
    capability_name: str,
) -> list[DeviceAttribute] | dict[str, str | list[str]]:
    """Get attributes for a specific capability.

    Args:
        capability_name: The name of the capability (extracted from URI)

    Returns:
        List of DeviceAttribute objects
    """
    # Get attributes for the capability
    attributes = CapabilityDataLoader.get_capability_attributes(capability_name)

    if attributes is None:
        return {
            "error": f"Capability '{capability_name}' not found",
            "available_capabilities": CapabilityDataLoader.get_all_capability_names(),
        }

    # Return the list of DeviceAttribute objects directly
    return attributes


@mcp.resource("hubitat://capabilities/{capability_name}/commands")
async def get_capability_commands(
    capability_name: str,
) -> list[DeviceCommand] | dict[str, str | list[str]]:
    """Get commands for a specific capability.

    Args:
        capability_name: The name of the capability (extracted from URI)

    Returns:
        List of DeviceCommand objects or error message
    """
    # Get commands for the capability
    commands = CapabilityDataLoader.get_capability_commands(capability_name)

    if commands is None:
        return {
            "error": f"Capability '{capability_name}' not found",
            "available_capabilities": CapabilityDataLoader.get_all_capability_names(),
        }

    # Return the list of DeviceCommand objects directly
    return commands
