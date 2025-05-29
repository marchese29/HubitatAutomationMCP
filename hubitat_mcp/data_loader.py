"""Data access utilities for the MCP server."""

from typing import Optional

from models import (
    DeviceCapability,
    DeviceAttribute,
    DeviceCommand,
    load_attributes,
    load_commands,
)


class CapabilityDataLoader:
    """Provides access to capability data with error handling."""

    @staticmethod
    def get_all_capability_names() -> list[str]:
        """Get a list of all capability names."""
        return DeviceCapability.allowed_capabilities()

    @staticmethod
    def get_capability_attributes(
        capability_name: str,
    ) -> Optional[list[DeviceAttribute]]:
        """Get attributes for a specific capability.

        Args:
            capability_name: The name of the capability

        Returns:
            List of DeviceAttribute objects, or None if capability not found
        """
        try:
            capability = DeviceCapability(capability_name)
            capability_attributes = load_attributes()
            return capability_attributes.get(capability, [])
        except ValueError:
            return None

    @staticmethod
    def get_capability_commands(capability_name: str) -> Optional[list[DeviceCommand]]:
        """Get commands for a specific capability.

        Args:
            capability_name: The name of the capability

        Returns:
            List of DeviceCommand objects, or None if capability not found
        """
        try:
            capability = DeviceCapability(capability_name)
            capability_commands = load_commands()
            return capability_commands.get(capability, [])
        except ValueError:
            return None

    @staticmethod
    def is_valid_capability(capability_name: str) -> bool:
        """Check if a capability name is valid.

        Args:
            capability_name: The name of the capability to check

        Returns:
            True if the capability exists, False otherwise
        """
        try:
            DeviceCapability(capability_name)
            return True
        except ValueError:
            return False
