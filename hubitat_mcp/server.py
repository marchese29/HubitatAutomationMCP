"""FastMCP server implementation for Hubitat capabilities."""

import asyncio
from typing import Any

from fastmcp import FastMCP

from hubitat import HubitatClient
from hubitat_mcp.data_loader import CapabilityDataLoader
from models.capabilities import DeviceAttribute, DeviceCommand
from models.devices import (
    CommandExecutionResult,
    CommandRequest,
    DeviceStateInfo,
    HubitatDeviceInfo,
)

# Initialize FastMCP server
mcp = FastMCP("Hubitat Capabilities")
client = HubitatClient()


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


@mcp.resource("hubitat://devices")
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
        for device in await client.get_all_devices()
    ]


# Helper function for safe command execution
async def _execute_command_safely(cmd: CommandRequest) -> CommandExecutionResult:
    """Execute a single command with error handling."""
    try:
        await client.send_command(cmd.device_id, cmd.command, cmd.arguments)
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
    all_devices = await client.get_all_devices()

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
