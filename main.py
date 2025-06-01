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


# Initialize FastMCP server
mcp = FastMCP("Hubitat Capabilities")

# Get the directory where this script is located
script_dir = Path(__file__).parent

# Load capability attributes file using absolute path
attributes_path = script_dir / "capability_attributes.json"
with open(attributes_path, "r") as f:
    file_content = f.read()
mcp.add_resource(
    TextResource(
        uri="hubitat://attributes",
        name="Capability Attributes",
        description="The device attributes for each capability",
        text=file_content,
    )
)

# Load capability commands file using absolute path
commands_path = script_dir / "capability_commands.json"
with open(commands_path, "r") as f:
    file_content = f.read()
mcp.add_resource(
    TextResource(
        uri="hubitat://commands",
        name="Capability Commands",
        description="The device commands for each capability",
        text=file_content,
    )
)


@mcp.resource("hubitat://capabilities", name="Capabilities")
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

    client = HubitatClient()
    return [
        HubitatDeviceInfo.from_hubitat_device(device)
        for device in await client.get_all_devices()
    ]


# Helper function for safe command execution
async def _execute_command_safely(
    client: HubitatClient, cmd: CommandRequest
) -> CommandExecutionResult:
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
    client = HubitatClient()
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
    client = HubitatClient()
    return await asyncio.gather(
        *[_execute_command_safely(client, cmd) for cmd in commands],
        return_exceptions=False,  # We handle exceptions in execute_command_safely
    )


if __name__ == "__main__":
    mcp.run()
