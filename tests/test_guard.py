"""Unit tests for SchemaGuard."""
import unittest
from mcp_schema_guard.guard import SchemaGuard

class TestSchemaGuard(unittest.TestCase):
    def setUp(self):
        self.guard = SchemaGuard()
        self.guard.register_tool("create_item", {
            "properties": {
                "name": {"type": "string"},
                "count": {"type": "integer"},
                "active": {"type": "boolean"}
            },
            "required": ["name", "count"]
        })

    def test_valid_call(self):
        ok, err, cleaned = self.guard.validate_call("create_item", {"name": "Widget", "count": 10, "active": True})
        self.assertTrue(ok)
        self.assertIsNone(err)
        self.assertEqual(cleaned["name"], "Widget")

    def test_missing_required(self):
        ok, err, cleaned = self.guard.validate_call("create_item", {"name": "Widget"})
        self.assertFalse(ok)
        self.assertIn("Missing required property", err)

    def test_type_coercion_and_stripping(self):
        ok, err, cleaned = self.guard.validate_call("create_item", {"name": "Gadget", "count": "25", "extra": "omit"})
        self.assertTrue(ok)
        self.assertEqual(cleaned["count"], 25)
        self.assertNotIn("extra", cleaned)

if __name__ == "__main__":
    unittest.main()
