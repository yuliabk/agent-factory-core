from __future__ import annotations

from typing import Mapping

from .tool_gateway import ToolRegistration, ToolSpec


SYNTHETIC_LOOKUP_INPUT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["key"],
    "properties": {
        "key": {"type": "string", "minLength": 1},
    },
}

SYNTHETIC_LOOKUP_OUTPUT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["found", "value"],
    "properties": {
        "found": {"type": "boolean"},
        "value": {"type": ["string", "null"]},
    },
}


def build_synthetic_lookup_tool(
    data: Mapping[str, str] | None = None,
) -> ToolRegistration:
    """Create a deterministic zero-side-effect lookup tool for contract tests."""
    dataset = dict(data or {"alpha": "A", "beta": "B"})

    def handler(payload: Mapping[str, object]) -> Mapping[str, object]:
        key = str(payload["key"])
        return {
            "found": key in dataset,
            "value": dataset.get(key),
        }

    return ToolRegistration(
        spec=ToolSpec(
            tool_ref="synthetic.lookup",
            binding_id="tool.synthetic.lookup.v1",
            version="1",
            required_permission="synthetic.lookup",
            minimum_trust_profile="sandbox",
            allowed_data_classifications=("public", "internal"),
            side_effect_class="read_only",
            input_schema=SYNTHETIC_LOOKUP_INPUT_SCHEMA,
            output_schema=SYNTHETIC_LOOKUP_OUTPUT_SCHEMA,
        ),
        handler=handler,
    )
