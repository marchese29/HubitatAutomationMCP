# Hubitat Automation MCP Server

> **Control your Hubitat smart home devices through AI assistants using the Model Context Protocol**

Transform your Hubitat smart home hub into an AI-controllable automation system. This MCP server enables LLM assistants like Claude to directly interact with your smart home devices for natural language control, monitoring, and automation.

## 🚀 Quick Start

Get your smart home AI-ready in under 5 minutes:

```bash
# 1. Clone and install
git clone <your-repo>
cd HubitatAutomationMCP
pip install -e .

# 2. Configure your Hubitat connection (see setup below)
export HE_ADDRESS="http://your-hubitat-ip"
export HE_APP_ID="your-app-id"  
export HE_ACCESS_TOKEN="your-token"

# 3. Run the MCP server
uv run fastmcp run main.py
```

**That's it!** Your AI assistant can now control lights, switches, sensors, and 100+ other device types.

## 🏠 What Can You Do?

Once connected, ask your AI assistant to:

- **"Turn off all the lights in the living room"**
- **"What's the temperature on the thermostat?"** 
- **"Lock the front door and arm the security system"**
- **"Show me which motion sensors detected activity today"**
- **"Set the bedroom lights to 30% brightness"**

The server supports **101 different device capabilities** including lights, switches, sensors, thermostats, locks, cameras, and more.

## 📋 Setup Instructions

### Prerequisites

- **Hubitat Elevation Hub** (C-4, C-5, C-7, or C-8)
- **Python 3.12+** 
- **Network access** to your Hubitat hub

### Step 1: Install the MCP Server

```bash
# Option A: Install from source
git clone <your-repo>
cd HubitatAutomationMCP
pip install -e .

# Option B: Using uv (recommended)
uv sync
```

### Step 2: Create Hubitat Maker API App

1. **Open your Hubitat hub** at `http://your-hubitat-ip`
2. **Go to Apps → Add Built-In App**
3. **Select "Maker API"**
4. **Choose your devices** to control (or select all)
5. **Enable "Allow Access via Local IP Address"**
6. **Save and note down:**
   - **App ID** (shown in the URL: `/installedapp/configure/{APP_ID}/`)
   - **Access Token** (shown in the app settings)

### Step 3: Configure Environment Variables

Create these environment variables with your Hubitat details:

```bash
# Your Hubitat hub's IP address
export HE_ADDRESS="http://192.168.1.100"

# From your Maker API app (step 2)
export HE_APP_ID="123"
export HE_ACCESS_TOKEN="your-long-access-token-here"
```

**For permanent setup**, add these to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.)

### Step 4: Test Your Connection

```bash
# Start the MCP server
uv run fastmcp run main.py

# In another terminal, test device discovery
curl "http://your-hubitat-ip/apps/api/123/devices?access_token=your-token"
```

If you see a JSON response with your devices, you're ready to go! 🎉

## 💡 Usage Examples

### Control Individual Devices

**Turn on a light:**
```
"Turn on the kitchen light"
```
*The AI will find device ID and send an "on" command*

**Set dimmer level:**
```
"Set the living room lamp to 75%"
```
*Sends setLevel command with value 75*

**Check device status:**
```
"What's the current temperature on the bedroom thermostat?"
```
*Retrieves device attributes and reports temperature*

### Control Multiple Devices

**Room-based control:**
```
"Turn off all lights in the bedroom"
```
*Finds all lights with "bedroom" in the name/room and sends "off" commands*

**Scene activation:**
```
"Set movie night: dim living room lights to 20%, turn off kitchen lights"
```
*Sends multiple commands in parallel*

### Monitor and Check Status

**Security check:**
```
"Are all doors locked and is the security system armed?"
```
*Checks lock and HSM device attributes*

**Environmental monitoring:**
```
"What's the temperature and humidity in each room?"
```
*Queries temperature/humidity sensors throughout the house*

## 🔧 Available Features

### Device Control Tools

- **`get_device_states`** - Check current status of any devices
- **`send_commands`** - Control devices (supports parallel execution)

### Information Resources  

- **Device Discovery** - Find all connected devices and their capabilities
- **Capability Reference** - 101 supported device types (lights, switches, sensors, etc.)
- **Attributes Guide** - Available status information (temperature, battery, etc.) 
- **Commands Reference** - Available control actions (on/off, setLevel, lock, etc.)

### Supported Device Types

✅ **Lighting**: Switches, dimmers, bulbs, LED strips  
✅ **Climate**: Thermostats, temperature sensors, humidity sensors  
✅ **Security**: Locks, motion sensors, contact sensors, cameras  
✅ **Safety**: Smoke detectors, water sensors, CO detectors  
✅ **Entertainment**: Speakers, TVs, media players  
✅ **Energy**: Smart plugs, energy monitors, power meters  
✅ **And 95+ more capabilities...**

## 🛠️ Troubleshooting

### "Connection refused" or timeout errors

**Check network connectivity:**
```bash
ping your-hubitat-ip
curl http://your-hubitat-ip
```

**Verify Maker API is enabled:**
- Go to Apps → Maker API in Hubitat interface
- Ensure "Allow Access via Local IP Address" is checked
- Try accessing the API URL directly in your browser

### "Unauthorized" or authentication errors

**Double-check your credentials:**
- **HE_APP_ID**: Should be a number (like `123`)
- **HE_ACCESS_TOKEN**: Should be a long string from Maker API app
- **HE_ADDRESS**: Should include `http://` and the correct IP

**Test with curl:**
```bash
curl "http://your-ip/apps/api/YOUR_APP_ID/devices?access_token=YOUR_TOKEN"
```

### Devices not responding to commands

**Verify device selection in Maker API:**
- Open your Maker API app in Hubitat
- Ensure the devices you want to control are selected
- Save the app after making changes

**Check device capabilities:**
- Some devices may not support certain commands
- Use the MCP resources to check available commands for each device type

### MCP server won't start

**Check Python version:**
```bash
python --version  # Should be 3.12+
```

**Install dependencies:**
```bash
pip install fastmcp httpx pydantic
# or
uv sync
```

## 🆘 Getting Help

### Quick Solutions

- **Device not found**: Check device name spelling and ensure it's selected in Maker API
- **Command failed**: Verify the device supports that command type
- **Slow responses**: Check network connection between server and Hubitat hub
- **Permission denied**: Ensure Maker API has "Local IP Address" access enabled

### Community Support

- **GitHub Issues**: Report bugs or request features
- **Hubitat Community**: Get help with device setup and configuration
- **MCP Documentation**: Learn more about Model Context Protocol

### Advanced Configuration

For developers or advanced users, see the technical documentation in the project's Memory Bank files for:
- Architecture details and code structure
- Extending capabilities and adding new device types  
- Performance optimization and scaling
- Integration with other home automation platforms

---

## 📈 What's Next?

**Coming Soon:**
- **Room Management System** - Organize devices by room with complex relationships
- **Automation Rules** - Create sophisticated if-then scenarios
- **Event Monitoring** - Real-time device status changes and notifications

**Get Started Today** and transform your smart home into an AI-controlled automation powerhouse! 🏡🤖