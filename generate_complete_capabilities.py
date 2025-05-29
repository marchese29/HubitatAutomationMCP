#!/usr/bin/env python3
"""
Generate complete capability JSON files with all 102 Hubitat capabilities.
Based on common patterns and the capability list from the documentation.
"""

import json
from typing import Dict, List, Any

# All 102 capabilities extracted from the Hubitat documentation
ALL_CAPABILITIES = [
    "AccelerationSensor",
    "Actuator",
    "AirQuality",
    "Alarm",
    "AudioNotification",
    "AudioVolume",
    "Battery",
    "Beacon",
    "Bulb",
    "Button (Deprecated)",
    "CarbonDioxideMeasurement",
    "CarbonMonoxideDetector",
    "ChangeLevel",
    "Chime",
    "ColorControl",
    "ColorMode",
    "ColorTemperature",
    "Configuration",
    "Consumable",
    "ContactSensor",
    "CurrentMeter",
    "DoorControl",
    "DoubleTapableButton",
    "EnergyMeter",
    "EstimatedTimeOfArrival",
    "FanControl",
    "FilterStatus",
    "Flash",
    "GarageDoorControl",
    "GasDetector",
    "HealthCheck",
    "HoldableButton",
    "IlluminanceMeasurement",
    "ImageCapture",
    "Indicator",
    "Initialize",
    "Light",
    "LightEffects",
    "LiquidFlowRate",
    "LocationMode",
    "Lock",
    "LockCodes",
    "MediaController",
    "MediaInputSource",
    "MediaTransport",
    "Momentary",
    "MotionSensor",
    "MusicPlayer",
    "Notification",
    "Outlet",
    "Polling",
    "PowerMeter",
    "PowerSource",
    "PresenceSensor",
    "PressureMeasurement",
    "PushableButton",
    "Refresh",
    "RelativeHumidityMeasurement",
    "RelaySwitch",
    "ReleasableButton",
    "SamsungTV",
    "SecurityKeypad",
    "Sensor",
    "ShockSensor",
    "SignalStrength",
    "SleepSensor",
    "SmokeDetector",
    "SoundPressureLevel",
    "SoundSensor",
    "SpeechRecognition",
    "SpeechSynthesis",
    "StepSensor",
    "Switch",
    "SwitchLevel",
    "TV",
    "TamperAlert",
    "Telnet",
    "TemperatureMeasurement",
    "TestCapability",
    "Thermostat",
    "ThermostatCoolingSetpoint",
    "ThermostatFanMode",
    "ThermostatHeatingSetpoint",
    "ThermostatMode",
    "ThermostatOperatingState",
    "ThermostatSchedule",
    "ThermostatSetpoint",
    "ThreeAxis",
    "TimedSession",
    "Tone",
    "TouchSensor",
    "UltravioletIndex",
    "Valve",
    "Variable",
    "VideoCamera",
    "VideoCapture",
    "VoltageMeasurement",
    "WaterSensor",
    "WindowBlind",
    "WindowShade",
    "ZwMultichannel",
    "pHMeasurement",
]


def generate_attributes_data() -> Dict[str, List[Dict[str, Any]]]:
    """Generate comprehensive attributes data for all capabilities."""

    attributes_data = {}

    # Define common attribute patterns
    attribute_patterns = {
        "AccelerationSensor": [
            {
                "name": "acceleration",
                "value_type": "string",
                "restrictions": {"enum": ["inactive", "active"]},
            }
        ],
        "Actuator": [],  # No specific attributes
        "AirQuality": [
            {"name": "airQuality", "value_type": "number"},
            {"name": "airQualityIndex", "value_type": "number"},
        ],
        "Alarm": [
            {
                "name": "alarm",
                "value_type": "string",
                "restrictions": {"enum": ["off", "strobe", "siren", "both"]},
            }
        ],
        "AudioNotification": [],
        "AudioVolume": [
            {
                "name": "volume",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 100},
            },
            {
                "name": "mute",
                "value_type": "string",
                "restrictions": {"enum": ["muted", "unmuted"]},
            },
        ],
        "Battery": [
            {
                "name": "battery",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 100},
            }
        ],
        "Beacon": [
            {
                "name": "presence",
                "value_type": "string",
                "restrictions": {"enum": ["present", "not present"]},
            }
        ],
        "Bulb": [
            {
                "name": "switch",
                "value_type": "string",
                "restrictions": {"enum": ["on", "off"]},
            }
        ],
        "Button (Deprecated)": [
            {
                "name": "button",
                "value_type": "string",
                "restrictions": {"enum": ["pushed"]},
            }
        ],
        "CarbonDioxideMeasurement": [{"name": "carbonDioxide", "value_type": "number"}],
        "CarbonMonoxideDetector": [
            {
                "name": "carbonMonoxide",
                "value_type": "string",
                "restrictions": {"enum": ["clear", "detected", "tested"]},
            }
        ],
        "ChangeLevel": [
            {
                "name": "level",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 100},
            }
        ],
        "Chime": [],
        "ColorControl": [
            {
                "name": "hue",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 360},
            },
            {
                "name": "saturation",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 100},
            },
            {"name": "color", "value_type": "string"},
        ],
        "ColorMode": [
            {
                "name": "colorMode",
                "value_type": "string",
                "restrictions": {"enum": ["RGB", "CT"]},
            }
        ],
        "ColorTemperature": [
            {
                "name": "colorTemperature",
                "value_type": "number",
                "restrictions": {"minimum": 2000, "maximum": 6500},
            }
        ],
        "Configuration": [],
        "Consumable": [
            {
                "name": "consumableStatus",
                "value_type": "string",
                "restrictions": {
                    "enum": ["good", "replace", "maintenance_required", "missing"]
                },
            }
        ],
        "ContactSensor": [
            {
                "name": "contact",
                "value_type": "string",
                "restrictions": {"enum": ["open", "closed"]},
            }
        ],
        "CurrentMeter": [{"name": "amperage", "value_type": "number"}],
        "DoorControl": [
            {
                "name": "door",
                "value_type": "string",
                "restrictions": {
                    "enum": ["open", "closed", "opening", "closing", "unknown"]
                },
            }
        ],
        "DoubleTapableButton": [
            {"name": "doubleTapped", "value_type": "number"},
            {"name": "numberOfButtons", "value_type": "number"},
        ],
        "EnergyMeter": [{"name": "energy", "value_type": "number"}],
        "EstimatedTimeOfArrival": [{"name": "eta", "value_type": "string"}],
        "FanControl": [
            {
                "name": "speed",
                "value_type": "string",
                "restrictions": {
                    "enum": [
                        "off",
                        "low",
                        "medium-low",
                        "medium",
                        "medium-high",
                        "high",
                        "on",
                        "auto",
                    ]
                },
            }
        ],
        "FilterStatus": [
            {
                "name": "filterStatus",
                "value_type": "string",
                "restrictions": {"enum": ["normal", "replace"]},
            }
        ],
        "Flash": [],
        "GarageDoorControl": [
            {
                "name": "door",
                "value_type": "string",
                "restrictions": {
                    "enum": ["open", "closed", "opening", "closing", "unknown"]
                },
            }
        ],
        "GasDetector": [
            {
                "name": "naturalGas",
                "value_type": "string",
                "restrictions": {"enum": ["clear", "detected", "tested"]},
            }
        ],
        "HealthCheck": [
            {"name": "checkInterval", "value_type": "number"},
            {
                "name": "healthStatus",
                "value_type": "string",
                "restrictions": {"enum": ["online", "offline"]},
            },
        ],
        "HoldableButton": [
            {"name": "held", "value_type": "number"},
            {"name": "numberOfButtons", "value_type": "number"},
        ],
        "IlluminanceMeasurement": [{"name": "illuminance", "value_type": "number"}],
        "ImageCapture": [{"name": "image", "value_type": "string"}],
        "Indicator": [
            {
                "name": "indicatorStatus",
                "value_type": "string",
                "restrictions": {"enum": ["when off", "when on", "never"]},
            }
        ],
        "Initialize": [],
        "Light": [
            {
                "name": "switch",
                "value_type": "string",
                "restrictions": {"enum": ["on", "off"]},
            }
        ],
        "LightEffects": [
            {"name": "effectName", "value_type": "string"},
            {"name": "effectNumber", "value_type": "number"},
        ],
        "LiquidFlowRate": [{"name": "rate", "value_type": "number"}],
        "LocationMode": [{"name": "mode", "value_type": "string"}],
        "Lock": [
            {
                "name": "lock",
                "value_type": "string",
                "restrictions": {
                    "enum": ["locked", "unlocked", "unlocked with timeout", "unknown"]
                },
            }
        ],
        "LockCodes": [
            {"name": "codeChanged", "value_type": "string"},
            {"name": "codeLength", "value_type": "number"},
            {"name": "lockCodes", "value_type": "string"},
            {"name": "maxCodes", "value_type": "number"},
        ],
        "MediaController": [
            {"name": "activities", "value_type": "string"},
            {"name": "currentActivity", "value_type": "string"},
        ],
        "MediaInputSource": [{"name": "inputSource", "value_type": "string"}],
        "MediaTransport": [
            {
                "name": "transportStatus",
                "value_type": "string",
                "restrictions": {"enum": ["playing", "paused", "stopped"]},
            }
        ],
        "Momentary": [],
        "MotionSensor": [
            {
                "name": "motion",
                "value_type": "string",
                "restrictions": {"enum": ["active", "inactive"]},
            }
        ],
        "MusicPlayer": [
            {
                "name": "status",
                "value_type": "string",
                "restrictions": {"enum": ["playing", "paused", "stopped"]},
            },
            {
                "name": "level",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 100},
            },
            {"name": "trackDescription", "value_type": "string"},
            {"name": "trackData", "value_type": "string"},
            {
                "name": "mute",
                "value_type": "string",
                "restrictions": {"enum": ["muted", "unmuted"]},
            },
        ],
        "Notification": [],
        "Outlet": [
            {
                "name": "switch",
                "value_type": "string",
                "restrictions": {"enum": ["on", "off"]},
            }
        ],
        "Polling": [],
        "PowerMeter": [{"name": "power", "value_type": "number"}],
        "PowerSource": [
            {
                "name": "powerSource",
                "value_type": "string",
                "restrictions": {"enum": ["battery", "dc", "mains", "unknown"]},
            }
        ],
        "PresenceSensor": [
            {
                "name": "presence",
                "value_type": "string",
                "restrictions": {"enum": ["present", "not present"]},
            }
        ],
        "PressureMeasurement": [{"name": "pressure", "value_type": "number"}],
        "PushableButton": [
            {"name": "pushed", "value_type": "number"},
            {"name": "numberOfButtons", "value_type": "number"},
        ],
        "Refresh": [],
        "RelativeHumidityMeasurement": [
            {
                "name": "humidity",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 100},
            }
        ],
        "RelaySwitch": [
            {
                "name": "switch",
                "value_type": "string",
                "restrictions": {"enum": ["on", "off"]},
            }
        ],
        "ReleasableButton": [
            {"name": "released", "value_type": "number"},
            {"name": "numberOfButtons", "value_type": "number"},
        ],
        "SamsungTV": [
            {
                "name": "switch",
                "value_type": "string",
                "restrictions": {"enum": ["on", "off"]},
            },
            {
                "name": "volume",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 100},
            },
            {
                "name": "mute",
                "value_type": "string",
                "restrictions": {"enum": ["muted", "unmuted"]},
            },
        ],
        "SecurityKeypad": [{"name": "securityKeypad", "value_type": "string"}],
        "Sensor": [],
        "ShockSensor": [
            {
                "name": "shock",
                "value_type": "string",
                "restrictions": {"enum": ["clear", "detected"]},
            }
        ],
        "SignalStrength": [
            {"name": "lqi", "value_type": "number"},
            {"name": "rssi", "value_type": "number"},
        ],
        "SleepSensor": [
            {
                "name": "sleeping",
                "value_type": "string",
                "restrictions": {"enum": ["sleeping", "not sleeping"]},
            }
        ],
        "SmokeDetector": [
            {
                "name": "smoke",
                "value_type": "string",
                "restrictions": {"enum": ["clear", "detected", "tested"]},
            }
        ],
        "SoundPressureLevel": [{"name": "soundPressureLevel", "value_type": "number"}],
        "SoundSensor": [
            {
                "name": "sound",
                "value_type": "string",
                "restrictions": {"enum": ["detected", "not detected"]},
            }
        ],
        "SpeechRecognition": [{"name": "phraseSpoken", "value_type": "string"}],
        "SpeechSynthesis": [],
        "StepSensor": [
            {"name": "goal", "value_type": "number"},
            {"name": "steps", "value_type": "number"},
        ],
        "Switch": [
            {
                "name": "switch",
                "value_type": "string",
                "restrictions": {"enum": ["on", "off"]},
            }
        ],
        "SwitchLevel": [
            {
                "name": "level",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 100},
            }
        ],
        "TV": [
            {
                "name": "switch",
                "value_type": "string",
                "restrictions": {"enum": ["on", "off"]},
            },
            {"name": "channel", "value_type": "string"},
            {
                "name": "volume",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 100},
            },
        ],
        "TamperAlert": [
            {
                "name": "tamper",
                "value_type": "string",
                "restrictions": {"enum": ["clear", "detected"]},
            }
        ],
        "Telnet": [],
        "TemperatureMeasurement": [{"name": "temperature", "value_type": "number"}],
        "TestCapability": [{"name": "test", "value_type": "string"}],
        "Thermostat": [
            {"name": "temperature", "value_type": "number"},
            {"name": "heatingSetpoint", "value_type": "number"},
            {"name": "coolingSetpoint", "value_type": "number"},
            {"name": "thermostatSetpoint", "value_type": "number"},
            {
                "name": "thermostatMode",
                "value_type": "string",
                "restrictions": {
                    "enum": ["off", "heat", "cool", "auto", "emergency heat"]
                },
            },
            {
                "name": "thermostatFanMode",
                "value_type": "string",
                "restrictions": {"enum": ["auto", "circulate", "on"]},
            },
            {
                "name": "thermostatOperatingState",
                "value_type": "string",
                "restrictions": {
                    "enum": [
                        "idle",
                        "heating",
                        "cooling",
                        "pending heat",
                        "pending cool",
                        "vent economizer",
                        "fan only",
                    ]
                },
            },
        ],
        "ThermostatCoolingSetpoint": [
            {"name": "coolingSetpoint", "value_type": "number"}
        ],
        "ThermostatFanMode": [
            {
                "name": "thermostatFanMode",
                "value_type": "string",
                "restrictions": {"enum": ["auto", "circulate", "on"]},
            }
        ],
        "ThermostatHeatingSetpoint": [
            {"name": "heatingSetpoint", "value_type": "number"}
        ],
        "ThermostatMode": [
            {
                "name": "thermostatMode",
                "value_type": "string",
                "restrictions": {
                    "enum": ["off", "heat", "cool", "auto", "emergency heat"]
                },
            }
        ],
        "ThermostatOperatingState": [
            {
                "name": "thermostatOperatingState",
                "value_type": "string",
                "restrictions": {
                    "enum": [
                        "idle",
                        "heating",
                        "cooling",
                        "pending heat",
                        "pending cool",
                        "vent economizer",
                        "fan only",
                    ]
                },
            }
        ],
        "ThermostatSchedule": [{"name": "schedule", "value_type": "string"}],
        "ThermostatSetpoint": [{"name": "thermostatSetpoint", "value_type": "number"}],
        "ThreeAxis": [{"name": "threeAxis", "value_type": "string"}],
        "TimedSession": [
            {
                "name": "sessionStatus",
                "value_type": "string",
                "restrictions": {"enum": ["stopped", "running", "paused"]},
            }
        ],
        "Tone": [],
        "TouchSensor": [
            {
                "name": "touch",
                "value_type": "string",
                "restrictions": {"enum": ["touched"]},
            }
        ],
        "UltravioletIndex": [{"name": "ultravioletIndex", "value_type": "number"}],
        "Valve": [
            {
                "name": "valve",
                "value_type": "string",
                "restrictions": {"enum": ["open", "closed"]},
            }
        ],
        "Variable": [{"name": "variable", "value_type": "string"}],
        "VideoCamera": [{"name": "camera", "value_type": "string"}],
        "VideoCapture": [{"name": "clip", "value_type": "string"}],
        "VoltageMeasurement": [{"name": "voltage", "value_type": "number"}],
        "WaterSensor": [
            {
                "name": "water",
                "value_type": "string",
                "restrictions": {"enum": ["dry", "wet"]},
            }
        ],
        "WindowBlind": [
            {
                "name": "windowBlind",
                "value_type": "string",
                "restrictions": {
                    "enum": [
                        "open",
                        "closed",
                        "opening",
                        "closing",
                        "partially open",
                        "unknown",
                    ]
                },
            }
        ],
        "WindowShade": [
            {
                "name": "windowShade",
                "value_type": "string",
                "restrictions": {
                    "enum": [
                        "open",
                        "closed",
                        "opening",
                        "closing",
                        "partially open",
                        "unknown",
                    ]
                },
            }
        ],
        "ZwMultichannel": [{"name": "epEvent", "value_type": "string"}],
        "pHMeasurement": [
            {
                "name": "pH",
                "value_type": "number",
                "restrictions": {"minimum": 0, "maximum": 14},
            }
        ],
    }

    # Generate attributes for all capabilities
    for capability in ALL_CAPABILITIES:
        if capability in attribute_patterns:
            attributes_data[capability] = attribute_patterns[capability]
        else:
            # Default empty list for capabilities without specific attributes
            attributes_data[capability] = []

    return attributes_data


def generate_commands_data() -> Dict[str, List[Dict[str, Any]]]:
    """Generate comprehensive commands data for all capabilities."""

    commands_data = {}

    # Define common command patterns
    command_patterns = {
        "AccelerationSensor": [],
        "Actuator": [],
        "AirQuality": [],
        "Alarm": [
            {"name": "off"},
            {"name": "strobe"},
            {"name": "siren"},
            {"name": "both"},
        ],
        "AudioNotification": [
            {
                "name": "playSound",
                "arguments": [{"name": "soundNumber", "type": "number"}],
            }
        ],
        "AudioVolume": [
            {"name": "setVolume", "arguments": [{"name": "volume", "type": "number"}]},
            {"name": "volumeUp"},
            {"name": "volumeDown"},
            {"name": "mute"},
            {"name": "unmute"},
        ],
        "Battery": [],
        "Beacon": [],
        "Bulb": [{"name": "on"}, {"name": "off"}],
        "Button (Deprecated)": [],
        "CarbonDioxideMeasurement": [],
        "CarbonMonoxideDetector": [],
        "ChangeLevel": [
            {
                "name": "startLevelChange",
                "arguments": [{"name": "direction", "type": "string"}],
            },
            {"name": "stopLevelChange"},
        ],
        "Chime": [
            {
                "name": "playSound",
                "arguments": [{"name": "soundNumber", "type": "number"}],
            }
        ],
        "ColorControl": [
            {"name": "setColor", "arguments": [{"name": "colorMap", "type": "object"}]},
            {"name": "setHue", "arguments": [{"name": "hue", "type": "number"}]},
            {
                "name": "setSaturation",
                "arguments": [{"name": "saturation", "type": "number"}],
            },
        ],
        "ColorMode": [
            {
                "name": "setColorMode",
                "arguments": [{"name": "colorMode", "type": "string"}],
            }
        ],
        "ColorTemperature": [
            {
                "name": "setColorTemperature",
                "arguments": [{"name": "colorTemperature", "type": "number"}],
            }
        ],
        "Configuration": [{"name": "configure"}],
        "Consumable": [
            {
                "name": "setConsumableStatus",
                "arguments": [{"name": "status", "type": "string"}],
            }
        ],
        "ContactSensor": [],
        "CurrentMeter": [],
        "DoorControl": [{"name": "open"}, {"name": "close"}],
        "DoubleTapableButton": [],
        "EnergyMeter": [],
        "EstimatedTimeOfArrival": [],
        "FanControl": [
            {"name": "setSpeed", "arguments": [{"name": "speed", "type": "string"}]}
        ],
        "FilterStatus": [],
        "Flash": [{"name": "flash"}],
        "GarageDoorControl": [{"name": "open"}, {"name": "close"}],
        "GasDetector": [],
        "HealthCheck": [{"name": "ping"}],
        "HoldableButton": [],
        "IlluminanceMeasurement": [],
        "ImageCapture": [{"name": "take"}],
        "Indicator": [
            {"name": "indicatorNever"},
            {"name": "indicatorWhenOn"},
            {"name": "indicatorWhenOff"},
        ],
        "Initialize": [{"name": "initialize"}],
        "Light": [{"name": "on"}, {"name": "off"}],
        "LightEffects": [
            {
                "name": "setEffect",
                "arguments": [{"name": "effectNumber", "type": "number"}],
            },
            {"name": "setNextEffect"},
            {"name": "setPreviousEffect"},
        ],
        "LiquidFlowRate": [],
        "LocationMode": [
            {
                "name": "setLocationMode",
                "arguments": [{"name": "mode", "type": "string"}],
            }
        ],
        "Lock": [{"name": "lock"}, {"name": "unlock"}],
        "LockCodes": [
            {
                "name": "setCode",
                "arguments": [
                    {"name": "codeNumber", "type": "number"},
                    {"name": "code", "type": "string"},
                    {"name": "name", "type": "string"},
                ],
            },
            {
                "name": "deleteCode",
                "arguments": [{"name": "codeNumber", "type": "number"}],
            },
            {"name": "getCodes"},
            {"name": "reloadAllCodes"},
        ],
        "MediaController": [
            {
                "name": "startActivity",
                "arguments": [{"name": "activity", "type": "string"}],
            },
            {"name": "getCurrentActivity"},
            {"name": "getAllActivities"},
        ],
        "MediaInputSource": [
            {
                "name": "setInputSource",
                "arguments": [{"name": "inputSource", "type": "string"}],
            }
        ],
        "MediaTransport": [
            {"name": "play"},
            {"name": "pause"},
            {"name": "stop"},
            {"name": "nextTrack"},
            {"name": "previousTrack"},
        ],
        "Momentary": [{"name": "push"}],
        "MotionSensor": [],
        "MusicPlayer": [
            {"name": "play"},
            {"name": "pause"},
            {"name": "stop"},
            {"name": "nextTrack"},
            {"name": "previousTrack"},
            {"name": "setLevel", "arguments": [{"name": "level", "type": "number"}]},
            {
                "name": "playTrack",
                "arguments": [{"name": "trackUri", "type": "string"}],
            },
            {"name": "setTrack", "arguments": [{"name": "trackUri", "type": "string"}]},
            {
                "name": "resumeTrack",
                "arguments": [{"name": "trackUri", "type": "string"}],
            },
            {
                "name": "restoreTrack",
                "arguments": [{"name": "trackUri", "type": "string"}],
            },
            {"name": "mute"},
            {"name": "unmute"},
        ],
        "Notification": [
            {
                "name": "deviceNotification",
                "arguments": [{"name": "text", "type": "string"}],
            }
        ],
        "Outlet": [{"name": "on"}, {"name": "off"}],
        "Polling": [{"name": "poll"}],
        "PowerMeter": [],
        "PowerSource": [],
        "PresenceSensor": [],
        "PressureMeasurement": [],
        "PushableButton": [],
        "Refresh": [{"name": "refresh"}],
        "RelativeHumidityMeasurement": [],
        "RelaySwitch": [{"name": "on"}, {"name": "off"}],
        "ReleasableButton": [],
        "SamsungTV": [
            {"name": "on"},
            {"name": "off"},
            {"name": "setVolume", "arguments": [{"name": "volume", "type": "number"}]},
            {"name": "volumeUp"},
            {"name": "volumeDown"},
            {"name": "mute"},
            {"name": "unmute"},
        ],
        "SecurityKeypad": [],
        "Sensor": [],
        "ShockSensor": [],
        "SignalStrength": [],
        "SleepSensor": [],
        "SmokeDetector": [],
        "SoundPressureLevel": [],
        "SoundSensor": [],
        "SpeechRecognition": [],
        "SpeechSynthesis": [
            {"name": "speak", "arguments": [{"name": "text", "type": "string"}]}
        ],
        "StepSensor": [],
        "Switch": [{"name": "on"}, {"name": "off"}],
        "SwitchLevel": [
            {"name": "setLevel", "arguments": [{"name": "level", "type": "number"}]},
            {
                "name": "setLevel",
                "arguments": [
                    {"name": "level", "type": "number"},
                    {"name": "duration", "type": "number"},
                ],
            },
        ],
        "TV": [
            {"name": "on"},
            {"name": "off"},
            {"name": "channelUp"},
            {"name": "channelDown"},
            {
                "name": "setChannel",
                "arguments": [{"name": "channel", "type": "string"}],
            },
            {"name": "volumeUp"},
            {"name": "volumeDown"},
            {"name": "setVolume", "arguments": [{"name": "volume", "type": "number"}]},
        ],
        "TamperAlert": [],
        "Telnet": [
            {"name": "sendMsg", "arguments": [{"name": "message", "type": "string"}]}
        ],
        "TemperatureMeasurement": [],
        "TestCapability": [{"name": "test"}],
        "Thermostat": [
            {
                "name": "setHeatingSetpoint",
                "arguments": [{"name": "temperature", "type": "number"}],
            },
            {
                "name": "setCoolingSetpoint",
                "arguments": [{"name": "temperature", "type": "number"}],
            },
            {
                "name": "setThermostatMode",
                "arguments": [{"name": "thermostatMode", "type": "string"}],
            },
            {
                "name": "setThermostatFanMode",
                "arguments": [{"name": "fanMode", "type": "string"}],
            },
            {"name": "heat"},
            {"name": "cool"},
            {"name": "auto"},
            {"name": "off"},
            {"name": "emergencyHeat"},
            {"name": "fanAuto"},
            {"name": "fanCirculate"},
            {"name": "fanOn"},
        ],
        "ThermostatCoolingSetpoint": [
            {
                "name": "setCoolingSetpoint",
                "arguments": [{"name": "temperature", "type": "number"}],
            }
        ],
        "ThermostatFanMode": [
            {
                "name": "setThermostatFanMode",
                "arguments": [{"name": "fanMode", "type": "string"}],
            },
            {"name": "fanAuto"},
            {"name": "fanCirculate"},
            {"name": "fanOn"},
        ],
        "ThermostatHeatingSetpoint": [
            {
                "name": "setHeatingSetpoint",
                "arguments": [{"name": "temperature", "type": "number"}],
            }
        ],
        "ThermostatMode": [
            {
                "name": "setThermostatMode",
                "arguments": [{"name": "thermostatMode", "type": "string"}],
            },
            {"name": "heat"},
            {"name": "cool"},
            {"name": "auto"},
            {"name": "off"},
            {"name": "emergencyHeat"},
        ],
        "ThermostatOperatingState": [],
        "ThermostatSchedule": [],
        "ThermostatSetpoint": [
            {
                "name": "setThermostatSetpoint",
                "arguments": [{"name": "temperature", "type": "number"}],
            }
        ],
        "ThreeAxis": [],
        "TimedSession": [
            {"name": "start"},
            {"name": "stop"},
            {"name": "pause"},
            {"name": "cancel"},
        ],
        "Tone": [{"name": "beep"}],
        "TouchSensor": [],
        "UltravioletIndex": [],
        "Valve": [{"name": "open"}, {"name": "close"}],
        "Variable": [
            {"name": "setVariable", "arguments": [{"name": "value", "type": "string"}]}
        ],
        "VideoCamera": [{"name": "on"}, {"name": "off"}, {"name": "take"}],
        "VideoCapture": [{"name": "capture"}],
        "VoltageMeasurement": [],
        "WaterSensor": [],
        "WindowBlind": [
            {"name": "open"},
            {"name": "close"},
            {
                "name": "setPosition",
                "arguments": [{"name": "position", "type": "number"}],
            },
        ],
        "WindowShade": [
            {"name": "open"},
            {"name": "close"},
            {
                "name": "setPosition",
                "arguments": [{"name": "position", "type": "number"}],
            },
        ],
        "ZwMultichannel": [{"name": "enableEpEvents"}, {"name": "disableEpEvents"}],
        "pHMeasurement": [],
    }

    # Generate commands for all capabilities
    for capability in ALL_CAPABILITIES:
        if capability in command_patterns:
            commands_data[capability] = command_patterns[capability]
        else:
            # Default empty list for capabilities without specific commands
            commands_data[capability] = []

    return commands_data


def main():
    """Generate complete capability JSON files."""

    print("Generating complete capability attributes...")
    attributes_data = generate_attributes_data()

    print("Generating complete capability commands...")
    commands_data = generate_commands_data()

    # Load existing data to preserve any manual additions
    try:
        with open("capability_attributes.json", "r") as f:
            existing_attrs = json.load(f)
        print(f"Loaded existing attributes for {len(existing_attrs)} capabilities")
    except FileNotFoundError:
        existing_attrs = {}

    try:
        with open("capability_commands.json", "r") as f:
            existing_cmds = json.load(f)
        print(f"Loaded existing commands for {len(existing_cmds)} capabilities")
    except FileNotFoundError:
        existing_cmds = {}

    # Merge with existing data (keep existing, add new)
    for capability, attrs in attributes_data.items():
        if capability not in existing_attrs:
            existing_attrs[capability] = attrs

    for capability, cmds in commands_data.items():
        if capability not in existing_cmds:
            existing_cmds[capability] = cmds

    # Write updated JSON files
    with open("capability_attributes.json", "w") as f:
        json.dump(existing_attrs, f, indent=4, sort_keys=True)

    with open("capability_commands.json", "w") as f:
        json.dump(existing_cmds, f, indent=4, sort_keys=True)

    print(
        f"✅ Updated capability_attributes.json with {len(existing_attrs)} capabilities"
    )
    print(f"✅ Updated capability_commands.json with {len(existing_cmds)} capabilities")
    print(f"🎉 Complete! Added {len(ALL_CAPABILITIES)} total Hubitat capabilities")


if __name__ == "__main__":
    main()
