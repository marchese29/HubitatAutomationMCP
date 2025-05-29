# Hubitat Capabilities MCP Server

A FastMCP server that provides access to Hubitat device capability information through three resources using the `hubitat://` URI scheme.

## Architecture

```
📁 models/                    # Shared models
├── __init__.py              # Export all models
├── capabilities.py          # Core capability models & data loading
└── devices.py              # Device-specific models

📁 hubitat_mcp/              # FastMCP server implementation
├── __init__.py              # Module exports
├── server.py               # FastMCP server with resources
├── data_loader.py          # Data access utilities
├── run_server.py           # Standalone server runner
└── README.md               # This file

📝 hubitat.py               # Updated to use shared models
```

## Available Resources

### 1. `hubitat://capabilities`
- **Description**: Get a list of all available Hubitat capabilities
- **URI**: `hubitat://capabilities`
- **Type**: Static resource
- **Returns**: JSON with capabilities array and count

**Example Response**:
```json
{
  "capabilities": [
    "AccelerationSensor",
    "Switch",
    "SwitchLevel",
    "..."
  ],
  "count": 101
}
```

### 2. `hubitat://capabilities/{capability_name}/attributes`
- **Description**: Get attribute information for a specific capability
- **URI**: `hubitat://capabilities/{capability_name}/attributes`
- **Type**: Templated resource
- **Parameters**:
  - `capability_name`: Name of the capability (e.g., "Switch")
- **Returns**: JSON with attribute details or error message

**Example URI**: `hubitat://capabilities/Switch/attributes`

**Example Response**:
```json
{
  "capability": "Switch",
  "attributes": [
    {
      "name": "switch",
      "value_type": "string",
      "restrictions": {
        "enum": ["on", "off"]
      }
    }
  ],
  "count": 1
}
```

### 3. `hubitat://capabilities/{capability_name}/commands`
- **Description**: Get command information for a specific capability
- **URI**: `hubitat://capabilities/{capability_name}/commands`
- **Type**: Templated resource
- **Parameters**:
  - `capability_name`: Name of the capability (e.g., "Switch")
- **Returns**: JSON with command details or error message

**Example URI**: `hubitat://capabilities/Switch/commands`

**Example Response**:
```json
{
  "capability": "Switch",
  "commands": [
    {"name": "on"},
    {"name": "off"}
  ],
  "count": 2
}
```

## Running the Server

### Standalone Mode
```bash
uv run python hubitat_mcp/run_server.py
```

### As Import
```python
from hubitat_mcp.server import mcp
# Use mcp with your MCP client
```

## Data Sources

The server loads capability data from:
- `capability_attributes.json` - Attribute definitions for all capabilities
- `capability_commands.json` - Command definitions for all capabilities

## Error Handling

Invalid capability names return helpful error messages with the list of available capabilities:

```json
{
  "error": "Capability 'InvalidName' not found",
  "available_capabilities": ["Switch", "Light", "..."]
}
```

## Resource Usage Examples

### Access all capabilities
```
hubitat://capabilities
```

### Access specific capability attributes
```
hubitat://capabilities/Switch/attributes
hubitat://capabilities/TemperatureMeasurement/attributes
hubitat://capabilities/ColorControl/attributes
```

### Access specific capability commands
```
hubitat://capabilities/Switch/commands
hubitat://capabilities/SwitchLevel/commands
hubitat://capabilities/ColorControl/commands
```

## Implementation Details

- **Framework**: FastMCP 2.5.1+
- **Models**: Pydantic-based with shared architecture
- **Data Loading**: Cached at startup for performance
- **Resource Type**: Uses FastMCP resources with templated URIs
- **URI Scheme**: Custom `hubitat://` scheme for intuitive access
- **JSON Output**: All responses are formatted JSON strings