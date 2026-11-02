"""Command line interface for mcp-schema-guard."""
import argparse
from .guard import SchemaGuard

def main():
    guard = SchemaGuard()
    guard.register_tool("fetch_user", {
        "properties": {"id": {"type": "integer"}, "role": {"type": "string"}},
        "required": ["id"]
    })
    valid, err, cleaned = guard.validate_call("fetch_user", {"id": "123", "role": "admin", "extra": "spam"})
    print("Schema guard operational. Valid:", valid, "Cleaned:", cleaned)

if __name__ == "__main__":
    main()
