# Room Management Architecture: JSON-Based DAG System

## Overview

This document outlines the architectural design for a JSON-based room management system using a Directed Acyclic Graph (DAG) structure. The system will be integrated into the existing Hubitat MCP server to provide room organization and device grouping capabilities.

## Data Structure Design

### JSON Schema
```json
{
  "rooms": {
    "Living Room": {
      "device_ids": [123, 456, 789],
      "description": "Main family gathering space",
      "notes": "Smart TV setup with voice control"
    },
    "Kitchen": {
      "device_ids": [101, 102],
      "description": "Cooking and dining area"
    }
  },
  "adjacency": {
    "Main Floor": ["Living Room", "Kitchen", "Dining Room"],
    "Living Room": ["Entertainment Center"],
    "Kitchen": []
  }
}
```

### Pydantic Data Models

```python
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class Room(BaseModel):
    """Individual room with devices and metadata."""
    device_ids: List[int] = Field(default_factory=list, description="List of Hubitat device IDs in this room")
    description: Optional[str] = Field(None, description="Optional room description")
    notes: Optional[str] = Field(None, description="Special notes about the room")

class RoomData(BaseModel):
    """Complete room system data structure."""
    rooms: Dict[str, Room] = Field(default_factory=dict, description="Room name to Room object mapping")
    adjacency: Dict[str, List[str]] = Field(default_factory=dict, description="Parent room to children room names mapping")
    
    class Config:
        json_schema_extra = {
            "example": {
                "rooms": {
                    "Living Room": {
                        "device_ids": [123, 456],
                        "description": "Main gathering space"
                    }
                },
                "adjacency": {
                    "Main Floor": ["Living Room", "Kitchen"]
                }
            }
        }
```

## Tool Interface Design

### Core Tools (5 tools total)

1. **`create_room(name: str, device_ids: List[int], description: Optional[str] = None, notes: Optional[str] = None)`**
   - Creates new room with specified devices
   - Validates room name uniqueness
   - Validates device IDs exist via Hubitat API
   - Returns success confirmation

2. **`get_devices_in_room(name: str) -> List[DeviceStateInfo]`**
   - Returns full device state information for room's devices
   - Integrates with existing `get_device_states()` tool
   - Provides current attribute values, not just device IDs
   - Returns empty list if room doesn't exist

3. **`add_devices_to_room(name: str, device_ids: List[int])`**
   - Adds devices to existing room's device list
   - Validates device IDs exist via Hubitat API
   - Prevents duplicate device assignments
   - Returns updated device count

4. **`add_room_relationships(parent_name: str, child_names: List[str])`**
   - Creates parent→children relationships in adjacency structure
   - Performs cycle detection before adding relationships
   - Validates all room names exist
   - Returns success confirmation or cycle error

5. **`delete_rooms(names: List[str])`**
   - Removes rooms and all their relationships
   - Cleans up adjacency references (both as parent and child)
   - Batch operation for efficiency
   - Returns list of successfully deleted rooms

## Implementation Architecture

### Core Manager Class

```python
class RoomManager:
    """Manages room data persistence and validation."""
    
    def __init__(self, file_path: Path = Path("rooms.json")):
        self.file_path = file_path
    
    # File operations
    async def load_rooms(self) -> RoomData:
        """Load room data from JSON file, creating empty structure if missing."""
        
    async def save_rooms(self, data: RoomData) -> None:
        """Atomically save room data to JSON file with backup."""
    
    # Validation
    def detect_cycle(self, parent: str, children: List[str], adjacency: Dict[str, List[str]]) -> bool:
        """Check if adding parent->children relationships would create cycles."""
        
    async def validate_devices_exist(self, device_ids: List[int]) -> bool:
        """Validate device IDs exist in Hubitat using existing client."""
    
    # Utility operations
    def remove_room_from_adjacency(self, room_name: str, adjacency: Dict[str, List[str]]) -> None:
        """Remove all references to room from adjacency structure."""
```

### Cycle Detection Algorithm

```python
def detect_cycle(self, parent: str, children: List[str], adjacency: Dict[str, List[str]]) -> bool:
    """
    Check if adding parent->children relationships would create cycles.
    Uses depth-first search to detect if any child can reach back to parent.
    """
    for child in children:
        if self._path_exists(child, parent, adjacency):
            return True
    return False

def _path_exists(self, start: str, target: str, adjacency: Dict[str, List[str]]) -> bool:
    """DFS to check if path exists from start to target."""
    visited = set()
    stack = [start]
    
    while stack:
        current = stack.pop()
        if current == target:
            return True
        if current in visited:
            continue
        visited.add(current)
        stack.extend(adjacency.get(current, []))
    
    return False
```

## Integration with Existing MCP Server

### File Structure
```
├── main.py                    # FastMCP server (existing)
├── models/
│   ├── devices.py            # Existing device models
│   ├── capabilities.py       # Existing capability models
│   └── rooms.py              # New room models
├── room_manager.py           # New room management logic
└── rooms.json                # New room data file
```

### Tool Registration Pattern
```python
# In main.py, following existing pattern
from room_manager import RoomManager

room_manager = RoomManager()

@mcp.tool()
async def create_room(name: str, device_ids: List[int], description: Optional[str] = None, notes: Optional[str] = None):
    """Create a new room with specified devices."""
    return await room_manager.create_room(name, device_ids, description, notes)

# ... additional room tools following same pattern
```

## Error Handling Strategy

- **File I/O Errors:** Graceful fallback to empty structure, detailed error messages
- **Cycle Detection:** Clear error messages indicating which relationship would cause cycle
- **Room Not Found:** Detailed error with list of available room names
- **Device Validation:** Integration with Hubitat API to verify device IDs exist
- **Concurrent Access:** Atomic file writes with temporary files and rename operations
- **Data Validation:** Pydantic model validation for all JSON data structures

## Advantages of This Approach

1. **Simplicity:** JSON file storage, no database dependencies
2. **Portability:** Human-readable format, version control friendly
3. **Consistency:** Pydantic models align with existing codebase patterns
4. **Performance:** Efficient in-memory operations, small data structures
5. **Integration:** Leverages existing device validation and state retrieval tools
6. **Flexibility:** DAG structure supports complex room hierarchies without cycles

## Migration Notes

This design replaces the previously planned SQLite approach documented in the decision log. The JSON-based approach provides better simplicity and portability while maintaining the core functionality for room management and device organization.

The tool interface is intentionally minimal to encourage LLM-driven room management through create/delete patterns rather than complex update operations.