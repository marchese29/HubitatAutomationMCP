"""FastMCP server implementation for Hubitat capabilities."""

import json

from fastmcp import FastMCP

from .data_loader import CapabilityDataLoader


# Initialize FastMCP server
mcp = FastMCP("Hubitat Capabilities")


@mcp.resource("hubitat://capabilities")
async def get_all_capabilities() -> str:
    """Get a list of all available Hubitat capabilities.

    Returns:
        JSON string containing an array of capability names
    """
    capabilities = CapabilityDataLoader.get_all_capability_names()

    return json.dumps(
        {"capabilities": capabilities, "count": len(capabilities)}, indent=2
    )


@mcp.resource("hubitat://capabilities/{capability_name}/attributes")
async def get_capability_attributes(capability_name: str) -> str:
    """Get attributes for a specific capability.

    Args:
        capability_name: The name of the capability (extracted from URI)

    Returns:
        JSON string containing capability attributes or error message
    """
    # Get attributes for the capability
    attributes = CapabilityDataLoader.get_capability_attributes(capability_name)

    if attributes is None:
        return json.dumps(
            {
                "error": f"Capability '{capability_name}' not found",
                "available_capabilities": CapabilityDataLoader.get_all_capability_names(),
            },
            indent=2,
        )

    # Convert DeviceAttribute objects to dict format
    attributes_data = []
    for attr in attributes:
        attr_dict = {"name": attr.name, "value_type": attr.value_type}
        if attr.restrictions:
            attr_dict["restrictions"] = attr.restrictions
        if attr.special_info:
            attr_dict["special_info"] = attr.special_info
        attributes_data.append(attr_dict)

    return json.dumps(
        {
            "capability": capability_name,
            "attributes": attributes_data,
            "count": len(attributes_data),
        },
        indent=2,
    )


@mcp.resource("hubitat://capabilities/{capability_name}/commands")
async def get_capability_commands(capability_name: str) -> str:
    """Get commands for a specific capability.

    Args:
        capability_name: The name of the capability (extracted from URI)

    Returns:
        JSON string containing capability commands or error message
    """
    # Get commands for the capability
    commands = CapabilityDataLoader.get_capability_commands(capability_name)

    if commands is None:
        return json.dumps(
            {
                "error": f"Capability '{capability_name}' not found",
                "available_capabilities": CapabilityDataLoader.get_all_capability_names(),
            },
            indent=2,
        )

    # Convert DeviceCommand objects to dict format
    commands_data = []
    for cmd in commands:
        cmd_dict = {"name": cmd.name}
        if cmd.arguments:
            args_data = []
            for arg in cmd.arguments:
                arg_dict = {
                    "name": arg.name,
                    "value_type": arg.value_type,
                    "required": arg.required,
                }
                if arg.restrictions:
                    arg_dict["restrictions"] = arg.restrictions
                args_data.append(arg_dict)
            cmd_dict["arguments"] = args_data
        commands_data.append(cmd_dict)

    return json.dumps(
        {
            "capability": capability_name,
            "commands": commands_data,
            "count": len(commands_data),
        },
        indent=2,
    )
