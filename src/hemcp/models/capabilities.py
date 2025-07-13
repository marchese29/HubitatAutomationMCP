"""Hubitat device capability models and data loading."""

import json
import os
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class DeviceCapability(str, Enum):
    """Enum of supported Hubitat device capabilities."""

    ACCELERATION_SENSOR = "AccelerationSensor"
    ACTUATOR = "Actuator"
    AIR_QUALITY = "AirQuality"
    ALARM = "Alarm"
    AUDIO_NOTIFICATION = "AudioNotification"
    AUDIO_VOLUME = "AudioVolume"
    BATTERY = "Battery"
    BEACON = "Beacon"
    BULB = "Bulb"
    CARBON_DIOXIDE_MEASUREMENT = "CarbonDioxideMeasurement"
    CARBON_MONOXIDE_DETECTOR = "CarbonMonoxideDetector"
    CHANGE_LEVEL = "ChangeLevel"
    CHIME = "Chime"
    COLOR_CONTROL = "ColorControl"
    COLOR_MODE = "ColorMode"
    COLOR_TEMPERATURE = "ColorTemperature"
    CONFIGURATION = "Configuration"
    CONSUMABLE = "Consumable"
    CONTACT_SENSOR = "ContactSensor"
    CURRENT_METER = "CurrentMeter"
    DOOR_CONTROL = "DoorControl"
    DOUBLE_TAPABLE_BUTTON = "DoubleTapableButton"
    ENERGY_METER = "EnergyMeter"
    ESTIMATED_TIME_OF_ARRIVAL = "EstimatedTimeOfArrival"
    FAN_CONTROL = "FanControl"
    FILTER_STATUS = "FilterStatus"
    FLASH = "Flash"
    GARAGE_DOOR_CONTROL = "GarageDoorControl"
    GAS_DETECTOR = "GasDetector"
    HEALTH_CHECK = "HealthCheck"
    HOLDABLE_BUTTON = "HoldableButton"
    ILLUMINANCE_MEASUREMENT = "IlluminanceMeasurement"
    IMAGE_CAPTURE = "ImageCapture"
    INDICATOR = "Indicator"
    INITIALIZE = "Initialize"
    LIGHT = "Light"
    LIGHT_EFFECTS = "LightEffects"
    LIQUID_FLOW_RATE = "LiquidFlowRate"
    LOCATION_MODE = "LocationMode"
    LOCK = "Lock"
    LOCK_CODES = "LockCodes"
    MEDIA_CONTROLLER = "MediaController"
    MEDIA_INPUT_SOURCE = "MediaInputSource"
    MEDIA_TRANSPORT = "MediaTransport"
    MOMENTARY = "Momentary"
    MOTION_SENSOR = "MotionSensor"
    MUSIC_PLAYER = "MusicPlayer"
    NOTIFICATION = "Notification"
    OUTLET = "Outlet"
    PH_MEASUREMENT = "pHMeasurement"
    POLLING = "Polling"
    POWER_METER = "PowerMeter"
    POWER_SOURCE = "PowerSource"
    PRESENCE_SENSOR = "PresenceSensor"
    PRESSURE_MEASUREMENT = "PressureMeasurement"
    PUSHABLE_BUTTON = "PushableButton"
    REFRESH = "Refresh"
    RELATIVE_HUMIDITY_MEASUREMENT = "RelativeHumidityMeasurement"
    RELAY_SWITCH = "RelaySwitch"
    RELEASABLE_BUTTON = "ReleasableButton"
    SAMSUNG_TV = "SamsungTV"
    SECURITY_KEYPAD = "SecurityKeypad"
    SENSOR = "Sensor"
    SHOCK_SENSOR = "ShockSensor"
    SIGNAL_STRENGTH = "SignalStrength"
    SLEEP_SENSOR = "SleepSensor"
    SMOKE_DETECTOR = "SmokeDetector"
    SOUND_PRESSURE_LEVEL = "SoundPressureLevel"
    SOUND_SENSOR = "SoundSensor"
    SPEECH_RECOGNITION = "SpeechRecognition"
    SPEECH_SYNTHESIS = "SpeechSynthesis"
    STEP_SENSOR = "StepSensor"
    SWITCH = "Switch"
    SWITCH_LEVEL = "SwitchLevel"
    TAMPER_ALERT = "TamperAlert"
    TELNET = "Telnet"
    TEMPERATURE_MEASUREMENT = "TemperatureMeasurement"
    TEST_CAPABILITY = "TestCapability"
    THERMOSTAT = "Thermostat"
    THERMOSTAT_COOLING_SETPOINT = "ThermostatCoolingSetpoint"
    THERMOSTAT_FAN_MODE = "ThermostatFanMode"
    THERMOSTAT_HEATING_SETPOINT = "ThermostatHeatingSetpoint"
    THERMOSTAT_MODE = "ThermostatMode"
    THERMOSTAT_OPERATING_STATE = "ThermostatOperatingState"
    THERMOSTAT_SCHEDULE = "ThermostatSchedule"
    THERMOSTAT_SETPOINT = "ThermostatSetpoint"
    THREE_AXIS = "ThreeAxis"
    TIMED_SESSION = "TimedSession"
    TONE = "Tone"
    TOUCH_SENSOR = "TouchSensor"
    TV = "TV"
    ULTRAVIOLET_INDEX = "UltravioletIndex"
    VALVE = "Valve"
    VARIABLE = "Variable"
    VIDEO_CAMERA = "VideoCamera"
    VIDEO_CAPTURE = "VideoCapture"
    VOLTAGE_MEASUREMENT = "VoltageMeasurement"
    WATER_SENSOR = "WaterSensor"
    WINDOW_BLIND = "WindowBlind"
    WINDOW_SHADE = "WindowShade"
    ZW_MULTICHANNEL = "ZwMultichannel"

    @classmethod
    def allowed_capabilities(cls) -> list[str]:
        """Return a list of all allowed capability values."""
        return [capability.value for capability in cls]


class DeviceAttribute(BaseModel):
    """Represents a device attribute with its properties and restrictions."""

    name: str
    value_type: str
    restrictions: Optional[dict[str, Any]] = None
    special_info: Optional[str] = None

    def __hash__(self):
        return hash(self.name)


class CommandArgument(BaseModel):
    """Represents an argument for a device command."""

    name: str
    value_type: str
    restrictions: dict[str, Any] = {}
    required: bool = False

    def __hash__(self):
        return hash(self.name)


class DeviceCommand(BaseModel):
    """Represents a command that can be sent to a device."""

    name: str
    arguments: Optional[list[CommandArgument]] = None

    def __hash__(self):
        return hash(self.name)


def load_json_file(filename: str) -> dict[str, Any]:
    """Load a JSON file from the project root directory."""
    # Get the project root directory (parent of models directory)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    file_path = os.path.join(project_root, filename)
    with open(file_path, "r") as f:
        return json.load(f)


def load_attributes() -> dict[DeviceCapability, list[DeviceAttribute]]:
    """Load device attributes from JSON and convert to the appropriate types."""
    json_data = load_json_file("capability_attributes.json")
    result: dict[DeviceCapability, list[DeviceAttribute]] = {}

    for cap_str, attributes in json_data.items():
        # Convert string to enum
        capability = DeviceCapability(cap_str)
        # Convert dict to DeviceAttribute objects
        attr_objects = [DeviceAttribute(**attr) for attr in attributes]
        result[capability] = attr_objects

    return result


def load_commands() -> dict[DeviceCapability, list[DeviceCommand]]:
    """Load device commands from JSON and convert to the appropriate types."""
    json_data = load_json_file("capability_commands.json")
    result: dict[DeviceCapability, list[DeviceCommand]] = {}

    for cap_str, commands in json_data.items():
        # Convert string to enum
        capability = DeviceCapability(cap_str)

        # Convert dict to DeviceCommand objects
        cmd_objects = []
        for cmd in commands:
            # Handle arguments if present
            if "arguments" in cmd:
                # Convert dict to CommandArgument objects, mapping "type" to "value_type"
                args = []
                for arg in cmd["arguments"]:
                    # Map "type" field to "value_type" for consistency
                    arg_data = dict(arg)
                    if "type" in arg_data:
                        arg_data["value_type"] = arg_data.pop("type")
                    args.append(CommandArgument(**arg_data))
                cmd_obj = DeviceCommand(name=cmd["name"], arguments=args)
            else:
                cmd_obj = DeviceCommand(name=cmd["name"])
            cmd_objects.append(cmd_obj)

        result[capability] = cmd_objects

    return result
