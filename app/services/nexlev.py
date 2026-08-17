"""
NexLev MCP (Model Context Protocol) integration for data automation and business logic.

This service provides a bridge between MoneyPrintTurbo and the NexLev MCP server,
enabling access to automation capabilities, data management, and workflow orchestration.

Docs: https://prod.dashboard.nexlev.io
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

import httpx
from loguru import logger

from app.config import config


class NexLevMCPService:
    """Service for communicating with NexLev MCP server."""

    def __init__(self):
        self.mcp_url = config.app.get("nexlev_mcp_url", "https://prod.dashboard.nexlev.io/api/mcp")
        self.api_key = config.app.get("nexlev_api_key", "")
        self.enabled = bool(self.api_key)
        self.timeout = 30
        self.session: Optional[httpx.AsyncClient] = None

    async def _get_session(self) -> httpx.AsyncClient:
        """Get or create an async HTTP session."""
        if self.session is None:
            self.session = httpx.AsyncClient(timeout=self.timeout)
        return self.session

    async def close(self):
        """Close the async session."""
        if self.session:
            await self.session.aclose()
            self.session = None

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for NexLev API requests."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "MoneyPrintTurbo/1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Call a tool exposed by the NexLev MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
            timeout: Optional timeout override (in seconds)

        Returns:
            Response from the MCP server
        """
        if not self.enabled:
            logger.warning("NexLev MCP is not configured. Set nexlev_api_key in config.")
            return {"success": False, "error": "NexLev MCP not configured"}

        try:
            session = await self._get_session()
            payload = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments,
                },
                "id": 1,
            }

            logger.info(f"Calling NexLev tool: {tool_name} with args: {arguments}")

            response = await session.post(
                self.mcp_url,
                json=payload,
                headers=self._get_headers(),
                timeout=timeout or self.timeout,
            )
            response.raise_for_status()
            result = response.json()

            if "error" in result:
                logger.error(f"NexLev MCP error: {result['error']}")
                return {"success": False, "error": result["error"]}

            logger.info(f"NexLev tool '{tool_name}' executed successfully")
            return {"success": True, "data": result.get("result")}

        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling NexLev MCP: {str(e)}")
            return {"success": False, "error": f"HTTP error: {str(e)}"}
        except Exception as e:
            logger.error(f"Error calling NexLev tool '{tool_name}': {str(e)}")
            return {"success": False, "error": str(e)}

    async def list_tools(self) -> Dict[str, Any]:
        """
        List all available tools from the NexLev MCP server.

        Returns:
            List of available tools
        """
        if not self.enabled:
            logger.warning("NexLev MCP is not configured.")
            return {"success": False, "error": "NexLev MCP not configured", "tools": []}

        try:
            session = await self._get_session()
            payload = {
                "jsonrpc": "2.0",
                "method": "tools/list",
                "id": 1,
            }

            response = await session.post(
                self.mcp_url,
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout,
            )
            response.raise_for_status()
            result = response.json()

            tools = result.get("result", {}).get("tools", [])
            logger.info(f"Retrieved {len(tools)} tools from NexLev MCP")
            return {"success": True, "tools": tools}

        except Exception as e:
            logger.error(f"Error listing NexLev tools: {str(e)}")
            return {"success": False, "error": str(e), "tools": []}

    async def automate_workflow(
        self,
        workflow_name: str,
        inputs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Trigger a NexLev automation workflow.

        Args:
            workflow_name: Name of the workflow to trigger
            inputs: Input data for the workflow

        Returns:
            Workflow execution result
        """
        return await self.call_tool("automation/trigger_workflow", {
            "workflow_name": workflow_name,
            "inputs": inputs,
        })

    async def get_data(
        self,
        resource_type: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        Retrieve data from NexLev.

        Args:
            resource_type: Type of resource to retrieve
            filters: Optional filters for the query
            limit: Maximum number of results

        Returns:
            Retrieved data
        """
        return await self.call_tool("data/get", {
            "resource_type": resource_type,
            "filters": filters or {},
            "limit": limit,
        })

    async def store_data(
        self,
        resource_type: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Store data in NexLev.

        Args:
            resource_type: Type of resource to store
            data: Data to store

        Returns:
            Storage result
        """
        return await self.call_tool("data/store", {
            "resource_type": resource_type,
            "data": data,
        })


# Singleton instance
nexlev_service = NexLevMCPService()


# Synchronous wrapper functions for backwards compatibility
def list_nexlev_tools() -> Dict[str, Any]:
    """List available NexLev tools (synchronous)."""
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(nexlev_service.list_tools())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(nexlev_service.list_tools())


def call_nexlev_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Call a NexLev tool (synchronous)."""
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(nexlev_service.call_tool(tool_name, arguments))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(nexlev_service.call_tool(tool_name, arguments))
