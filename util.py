import os
import sys
from typing import Optional

from models import (
    DeviceCapability,
    DeviceAttribute,
    DeviceCommand,
    load_attributes,
    load_commands,
)


def env_var(name: str, allow_null: bool = False) -> str | None:
    """A useful utility for validating the presence of an environment variable before
    loading"""
    if not allow_null and name not in os.environ:
        sys.exit(f"{name} was not set in the environment")
    if allow_null and name not in os.environ:
        return None
    value = os.environ[name]
    if not allow_null and value is None:
        sys.exit(f"The value of {name} in the environment cannot be empty")
    return value


"""Data access utilities for the MCP server."""


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
