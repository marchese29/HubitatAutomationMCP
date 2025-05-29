#!/usr/bin/env python3
"""
Script to parse Hubitat capabilities from the downloaded HTML and generate
complete JSON files for attributes and commands.
"""

import re
import json
from collections import defaultdict
from typing import Dict, List, Any, Optional


def parse_enum_values(text: str) -> Optional[List[str]]:
    """Extract enum values from text like 'ENUM ["value1", "value2"]'"""
    enum_match = re.search(r"ENUM\s*\[([^\]]+)\]", text)
    if enum_match:
        values_str = enum_match.group(1)
        # Extract quoted values
        values = re.findall(r'"([^"]*)"', values_str)
        return values
    return None


def parse_range_values(text: str) -> Optional[Dict[str, Any]]:
    """Extract range values from text like 'range:0..500'"""
    range_match = re.search(r"range:(\d+(?:\.\d+)?)\.\.(\d+(?:\.\d+)?)", text)
    if range_match:
        min_val = range_match.group(1)
        max_val = range_match.group(2)
        # Convert to int if whole numbers, float otherwise
        try:
            min_val = int(min_val) if "." not in min_val else float(min_val)
            max_val = int(max_val) if "." not in max_val else float(max_val)
            return {"minimum": min_val, "maximum": max_val}
        except ValueError:
            pass
    return None


def determine_value_type(type_text: str) -> str:
    """Determine the value type from the type text"""
    type_text = type_text.upper()
    if "ENUM" in type_text:
        return "string"
    elif "NUMBER" in type_text or "INTEGER" in type_text:
        return "number" if "NUMBER" in type_text else "integer"
    elif "STRING" in type_text:
        return "string"
    elif "BOOLEAN" in type_text:
        return "boolean"
    else:
        return "string"  # default


def parse_capability_section(
    html_content: str,
) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """Parse the HTML content to extract capability attributes and commands"""

    attributes_data = {}
    commands_data = {}

    # Split content by capability sections (h2 headers)
    capability_sections = re.split(r'<h2[^>]*id="([^"]*)"[^>]*>', html_content)

    for i in range(1, len(capability_sections), 2):
        if i + 1 >= len(capability_sections):
            break

        capability_id = capability_sections[i]
        section_content = capability_sections[i + 1]

        # Extract capability name from the section content
        name_match = re.search(r"<[^>]*>([^<]+)</[^>]*>", section_content)
        if not name_match:
            continue

        capability_name = name_match.group(1).strip()
        if capability_name == "¶":  # Skip anchor symbols
            continue

        print(f"Processing capability: {capability_name}")

        # Find attributes section
        attributes_match = re.search(
            r'<h3[^>]*id="attributes[^"]*"[^>]*>.*?</h3>(.*?)(?=<h3|$)',
            section_content,
            re.DOTALL,
        )
        if attributes_match:
            attributes_content = attributes_match.group(1)
            attributes = parse_attributes_from_content(attributes_content)
            if attributes:
                attributes_data[capability_name] = attributes

        # Find commands section
        commands_match = re.search(
            r'<h3[^>]*id="commands[^"]*"[^>]*>.*?</h3>(.*?)(?=<h2|$)',
            section_content,
            re.DOTALL,
        )
        if commands_match:
            commands_content = commands_match.group(1)
            commands = parse_commands_from_content(commands_content)
            commands_data[capability_name] = commands

    return attributes_data, commands_data


def parse_attributes_from_content(content: str) -> List[Dict[str, Any]]:
    """Parse attributes from the content section"""
    attributes = []

    # Look for list items with attribute definitions
    attr_items = re.findall(r"<li><code>([^<]+)</code>\s*-\s*([^<]*)</li>", content)

    for attr_name, attr_type in attr_items:
        attr_def = {"name": attr_name, "value_type": determine_value_type(attr_type)}

        # Check for enum values
        enum_values = parse_enum_values(attr_type)
        if enum_values:
            attr_def["restrictions"] = {"enum": enum_values}

        # Check for range values
        range_values = parse_range_values(attr_type)
        if range_values:
            attr_def["restrictions"] = range_values

        attributes.append(attr_def)

    return attributes


def parse_commands_from_content(content: str) -> List[Dict[str, Any]]:
    """Parse commands from the content section"""
    commands = []

    # Look for list items with command definitions
    cmd_items = re.findall(r"<li><code>([^<(]+)(?:\(([^)]*)\))?</code>", content)

    for cmd_name, args_str in cmd_items:
        cmd_def = {"name": cmd_name.strip()}

        # Parse arguments if present
        if args_str and args_str.strip():
            # This is simplified - in reality we'd need more complex parsing
            # For now, we'll just note that there are arguments
            cmd_def["arguments"] = []

        commands.append(cmd_def)

    return commands


def main():
    """Main function to parse capabilities and generate JSON files"""

    # Read the HTML file
    try:
        with open("hubitat_capabilities.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: hubitat_capabilities.html not found")
        return

    # Parse the content
    print("Parsing capabilities...")
    attributes_data, commands_data = parse_capability_section(html_content)

    print(f"Found {len(attributes_data)} capabilities with attributes")
    print(f"Found {len(commands_data)} capabilities with commands")

    # Load existing data to preserve manual additions
    try:
        with open("capability_attributes.json", "r") as f:
            existing_attrs = json.load(f)
    except FileNotFoundError:
        existing_attrs = {}

    try:
        with open("capability_commands.json", "r") as f:
            existing_cmds = json.load(f)
    except FileNotFoundError:
        existing_cmds = {}

    # Merge with existing data (new data takes precedence)
    existing_attrs.update(attributes_data)
    existing_cmds.update(commands_data)

    # Write updated JSON files
    with open("capability_attributes.json", "w") as f:
        json.dump(existing_attrs, f, indent=4, sort_keys=True)

    with open("capability_commands.json", "w") as f:
        json.dump(existing_cmds, f, indent=4, sort_keys=True)

    print("Updated capability_attributes.json and capability_commands.json")


if __name__ == "__main__":
    main()
