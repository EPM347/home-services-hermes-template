#!/usr/bin/env python3
"""Local stdio MCP bridge over the authenticated Composio CLI.

Composio's hosted Connect MCP (https://connect.composio.dev/mcp) currently
returns 401 for consumer/API keys (known platform issue). This bridge exposes
a small, stable tool surface so Hermes can use your already-linked apps
(Gmail, Drive, GitHub, etc.) without the broken remote endpoint.

Tools:
  composio_search       - find tools by natural-language use case
  composio_execute      - run a tool slug with JSON args
  composio_connections  - list toolkit connection statuses
  composio_tools_list   - list tools in a toolkit
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from typing import Any


COMPOSIO = os.environ.get("COMPOSIO_BIN") or shutil.which("composio") or os.path.expanduser("~/.composio/composio")
DEFAULT_TIMEOUT = int(os.environ.get("COMPOSIO_MCP_TIMEOUT", "180"))


def _run(args: list[str], timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    if not os.path.isfile(COMPOSIO) and not shutil.which(COMPOSIO):
        return {"ok": False, "error": f"composio binary not found at {COMPOSIO}"}
    env = os.environ.copy()
    install_dir = os.path.expanduser("~/.composio")
    env.setdefault("COMPOSIO_INSTALL_DIR", install_dir)
    env["PATH"] = f"{install_dir}:{env.get('PATH', '')}"
    try:
        proc = subprocess.run(
            [COMPOSIO, *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"composio timed out after {timeout}s", "args": args}
    except Exception as e:
        return {"ok": False, "error": str(e), "args": args}

    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    payload: Any
    if stdout:
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError:
            payload = stdout
    else:
        payload = None

    return {
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "data": payload,
        "stderr": stderr[-4000:] if stderr else "",
        "args": args,
    }


def _tool_text(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)[:120000]


async def main() -> None:
    try:
        from mcp.server import Server
        from mcp.server.stdio import stdio_server
        from mcp import types
    except ImportError as e:
        print(f"mcp package required: {e}", file=sys.stderr)
        sys.exit(1)

    server = Server("composio-cli-bridge")

    tools = [
        types.Tool(
            name="composio_search",
            description=(
                "Search Composio tools by natural-language use case across 1000+ apps. "
                "Returns recommended tool slugs, plans, pitfalls, and connected toolkits. "
                "Use before composio_execute when you don't know the exact slug."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Use-case query, e.g. 'fetch unread gmail' or 'create github issue'",
                    },
                    "toolkits": {
                        "type": "string",
                        "description": "Optional comma-separated toolkit filter, e.g. 'gmail,github'",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (default 5)",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="composio_execute",
            description=(
                "Execute a Composio tool by slug with JSON arguments. "
                "Example slugs: GMAIL_FETCH_EMAILS, GITHUB_CREATE_ISSUE, GOOGLEDRIVE_FIND_FILE. "
                "Use composio_search first if unsure. Requires the toolkit account to be linked."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "slug": {
                        "type": "string",
                        "description": "Tool slug, e.g. GMAIL_FETCH_EMAILS",
                    },
                    "data": {
                        "type": "object",
                        "description": "JSON object of tool arguments (schema depends on slug)",
                        "additionalProperties": True,
                    },
                    "dry_run": {
                        "type": "boolean",
                        "description": "If true, validate only without executing",
                        "default": False,
                    },
                },
                "required": ["slug"],
            },
        ),
        types.Tool(
            name="composio_connections",
            description="List Composio toolkit connection statuses (ACTIVE/EXPIRED) for this account.",
            inputSchema={
                "type": "object",
                "properties": {
                    "toolkit": {
                        "type": "string",
                        "description": "Optional toolkit slug to filter, e.g. gmail",
                    }
                },
            },
        ),
        types.Tool(
            name="composio_tools_list",
            description="List available tools for a connected toolkit.",
            inputSchema={
                "type": "object",
                "properties": {
                    "toolkit": {
                        "type": "string",
                        "description": "Toolkit slug, e.g. gmail, github, notion",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max tools to return (default 30)",
                        "default": 30,
                    },
                    "query": {
                        "type": "string",
                        "description": "Optional filter query within the toolkit",
                    },
                },
                "required": ["toolkit"],
            },
        ),
    ]

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent]:
        args = arguments or {}
        if name == "composio_search":
            query = str(args.get("query") or "").strip()
            if not query:
                result = {"ok": False, "error": "query is required"}
            else:
                cmd = ["search", query, "--limit", str(int(args.get("limit") or 5))]
                toolkits = str(args.get("toolkits") or "").strip()
                if toolkits:
                    cmd.extend(["--toolkits", toolkits])
                result = _run(cmd)
        elif name == "composio_execute":
            slug = str(args.get("slug") or "").strip()
            if not slug:
                result = {"ok": False, "error": "slug is required"}
            else:
                data = args.get("data") or {}
                if not isinstance(data, dict):
                    result = {"ok": False, "error": "data must be a JSON object"}
                else:
                    cmd = ["execute", slug, "-d", json.dumps(data)]
                    if args.get("dry_run"):
                        cmd.append("--dry-run")
                    result = _run(cmd, timeout=max(DEFAULT_TIMEOUT, 240))
        elif name == "composio_connections":
            cmd = ["connections", "list"]
            toolkit = str(args.get("toolkit") or "").strip()
            if toolkit:
                cmd.extend(["--toolkit", toolkit])
            result = _run(cmd)
        elif name == "composio_tools_list":
            toolkit = str(args.get("toolkit") or "").strip()
            if not toolkit:
                result = {"ok": False, "error": "toolkit is required"}
            else:
                cmd = ["tools", "list", toolkit, "--limit", str(int(args.get("limit") or 30))]
                query = str(args.get("query") or "").strip()
                if query:
                    cmd.extend(["--query", query])
                result = _run(cmd)
        else:
            result = {"ok": False, "error": f"unknown tool: {name}"}

        return [types.TextContent(type="text", text=_tool_text(result))]

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
