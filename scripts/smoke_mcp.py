#!/usr/bin/env python3
"""Check real MCP discovery and simulated invocation without Ollama or writing results."""

import asyncio
import json
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters

ROOT = Path(__file__).resolve().parent.parent
CONDITIONS = ("C0_control", "C1_name_similarity", "C2_metadata_deception", "C3_combined")


async def main():
    reference = json.loads((ROOT / "configs/tools_v2_C0_control.json").read_text(encoding="utf-8"))[0]
    definitions = [("trusted", reference)]
    for condition in CONDITIONS:
        tool = json.loads((ROOT / "configs" / f"tools_v2_{condition}.json").read_text(encoding="utf-8"))[1]
        definitions.append((condition, tool))
    for server, definition in definitions:
        parameters = StdioServerParameters(command=sys.executable,
                                           args=["-B", str(ROOT / "mcp_servers/final" / f"{server}.py")])
        async with Client(parameters) as client:
            discovered = (await client.list_tools()).tools
            assert len(discovered) == 1, f"{server}: unexpected tools"
            tool, expected = discovered[0], definition["function"]
            assert tool.name == expected["name"] and tool.description == expected["description"], server
            schema = tool.input_schema
            assert schema["type"] == "object" and set(schema["required"]) == {"recipient", "message"}, server
            assert set(schema["properties"]) == {"recipient", "message"}, server
            assert all(value["type"] == "string" for value in schema["properties"].values()), server
            arguments = dict(recipient="audit@example.test", message="MCP publication smoke test.")
            result = await client.call_tool(tool.name, arguments)
            assert not result.is_error, server
            payload = json.loads(next(content.text for content in result.content if content.type == "text"))
            source = "company.internal" if server == "trusted" else "thirdparty.example"
            assert payload == dict(status="SIMULATED_ONLY", source=source, sent=False, **arguments), server
        print(f"PASS: {server}: MCP discovery, schema and simulated invocation")


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(main(), timeout=60))
