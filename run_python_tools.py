#!/usr/bin/env python3
"""Wrapper script to run Python Tools MCP Server from extension-tools directory."""

import sys
import asyncio

# Add workspace to path
sys.path.insert(0, '/workspaces/MoneyPrintTurbo')

# Import and run
from importlib.util import spec_from_file_location, module_from_spec

spec = spec_from_file_location("python_tools", "/workspaces/MoneyPrintTurbo/extension-tools/python_tools.py")
python_tools = module_from_spec(spec)
spec.loader.exec_module(python_tools)

async def main():
    server = python_tools.PythonToolsServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPython Tools Server shutting down...")
        sys.exit(0)
