"""Schema verification and parameter sanitation."""
from typing import Dict, Any, List, Optional, Tuple

class SchemaGuard:
    def __init__(self):
        self.schemas: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, schema: Dict[str, Any]) -> None:
        self.schemas[name] = schema

    def validate_call(self, tool_name: str, arguments: Dict[str, Any]) -> Tuple[bool, Optional[str], Dict[str, Any]]:
        if tool_name not in self.schemas:
            return True, None, arguments

        schema = self.schemas[tool_name]
        props = schema.get("properties", {})
        required = schema.get("required", [])

        # Check required fields
        for req in required:
            if req not in arguments:
                return False, f"Missing required property: '{req}'", {}

        sanitized: Dict[str, Any] = {}
        for key, val in arguments.items():
            if key not in props:
                continue  # strip unknown argument
            expected_type = props[key].get("type")
            if expected_type == "integer" and not isinstance(val, int):
                try:
                    val = int(val)
                except (ValueError, TypeError):
                    return False, f"Property '{key}' must be an integer", {}
            elif expected_type == "string" and not isinstance(val, str):
                val = str(val)
            elif expected_type == "boolean" and not isinstance(val, bool):
                val = str(val).lower() in ("true", "1")
            sanitized[key] = val

        return True, None, sanitized
