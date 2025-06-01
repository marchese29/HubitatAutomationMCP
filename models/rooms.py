"""Pydantic models for room management system."""

from typing import Optional
from pydantic import BaseModel, Field


class Room(BaseModel):
    """Individual room with devices and metadata."""

    device_ids: list[int] = Field(
        default_factory=list, description="List of Hubitat device IDs in this room"
    )
    description: Optional[str] = Field(None, description="Optional room description")
    notes: Optional[str] = Field(None, description="Special notes about the room")


class RoomData(BaseModel):
    """Complete room system data structure."""

    rooms: dict[str, Room] = Field(
        default_factory=dict, description="Room name to Room object mapping"
    )
    adjacency: dict[str, list[str]] = Field(
        default_factory=dict, description="Parent room to children room names mapping"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "rooms": {
                    "Living Room": {
                        "device_ids": [123, 456],
                        "description": "Main gathering space",
                        "notes": "Has smart TV setup",
                    },
                    "Kitchen": {
                        "device_ids": [101, 102],
                        "description": "Cooking area",
                    },
                },
                "adjacency": {
                    "Main Floor": ["Living Room", "Kitchen"],
                    "Living Room": ["Entertainment Center"],
                    "Kitchen": [],
                },
            }
        }
