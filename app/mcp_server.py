#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Server for MoneyPrintTurbo.

This server exposes MoneyPrintTurbo services as MCP tools that can be called
by Claude and other MCP-compatible clients.

Tools exposed:
- Video generation and publishing
- YouTube channel integration
- NexLev automation workflows
- GitHub repository management
- Content analysis and optimization

Usage:
  python3 app/mcp_server.py
"""

import sys
import json
import asyncio
import logging
from typing import Any, Dict, List, Optional

from loguru import logger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger.enable("app")


class MCPServer:
    """MCP Server implementation for MoneyPrintTurbo."""

    def __init__(self):
        self.tools = self._register_tools()
        self.version = "1.0.0"

    def _register_tools(self) -> Dict[str, Dict[str, Any]]:
        """Register all available tools."""
        return {
            # Video Generation Tools
            "generate_video": {
                "description": "Generate a video from text input",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "Video subject/topic",
                        },
                        "platforms": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Target platforms (youtube, tiktok, instagram)",
                        },
                        "video_source": {
                            "type": "string",
                            "enum": ["pexels", "pixabay", "coverr"],
                            "description": "Video material source",
                        },
                    },
                    "required": ["subject"],
                },
            },
            # YouTube Tools
            "publish_to_youtube": {
                "description": "Publish a video to YouTube channel",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "video_path": {
                            "type": "string",
                            "description": "Path to video file",
                        },
                        "title": {
                            "type": "string",
                            "description": "Video title",
                        },
                        "description": {
                            "type": "string",
                            "description": "Video description",
                        },
                        "privacy_status": {
                            "type": "string",
                            "enum": ["public", "unlisted", "private"],
                            "description": "Video privacy status",
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Video tags/keywords",
                        },
                    },
                    "required": ["video_path", "title"],
                },
            },
            "get_youtube_channel_info": {
                "description": "Get information about the YouTube channel",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                },
            },
            # NexLev Tools
            "call_nexlev_tool": {
                "description": "Call a NexLev MCP tool for automation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tool_name": {
                            "type": "string",
                            "description": "Name of the NexLev tool to call",
                        },
                        "arguments": {
                            "type": "object",
                            "description": "Arguments for the tool",
                        },
                    },
                    "required": ["tool_name"],
                },
            },
            "list_nexlev_tools": {
                "description": "List all available NexLev MCP tools",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                },
            },
            # GitHub Tools
            "get_repository_info": {
                "description": "Get information about the GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                },
            },
            "get_recent_commits": {
                "description": "Get recent commits from the repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "count": {
                            "type": "integer",
                            "description": "Number of commits to retrieve",
                            "default": 10,
                        },
                    },
                },
            },
            "create_github_issue": {
                "description": "Create a GitHub issue",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Issue title",
                        },
                        "body": {
                            "type": "string",
                            "description": "Issue description",
                        },
                        "labels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Issue labels",
                        },
                    },
                    "required": ["title"],
                },
            },
            # Content Analysis Tools
            "analyze_content_performance": {
                "description": "Analyze performance of generated content",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "metrics": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Metrics to analyze (views, engagement, etc.)",
                        },
                    },
                },
            },
        }

    def handle_tools_list(self) -> Dict[str, Any]:
        """Handle tools/list request."""
        return {
            "tools": [
                {
                    "name": name,
                    "description": tool.get("description", ""),
                    "inputSchema": tool.get("inputSchema", {}),
                }
                for name, tool in self.tools.items()
            ]
        }

    async def handle_tools_call(
        self,
        name: str,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Handle tools/call request."""
        logger.info(f"Calling tool: {name} with args: {arguments}")

        try:
            if name == "generate_video":
                return await self._generate_video(arguments)
            elif name == "publish_to_youtube":
                return await self._publish_to_youtube(arguments)
            elif name == "get_youtube_channel_info":
                return await self._get_youtube_channel_info()
            elif name == "call_nexlev_tool":
                return await self._call_nexlev_tool(arguments)
            elif name == "list_nexlev_tools":
                return await self._list_nexlev_tools()
            elif name == "get_repository_info":
                return await self._get_repository_info()
            elif name == "get_recent_commits":
                return await self._get_recent_commits(arguments)
            elif name == "create_github_issue":
                return await self._create_github_issue(arguments)
            elif name == "analyze_content_performance":
                return await self._analyze_content_performance(arguments)
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {name}",
                }
        except Exception as e:
            logger.error(f"Error executing tool {name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
            }

    async def _generate_video(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle video generation request."""
        try:
            from app.services.task import task_service

            subject = args.get("subject", "")
            platforms = args.get("platforms", ["youtube"])
            video_source = args.get("video_source", "pexels")

            if not subject:
                return {"success": False, "error": "Subject is required"}

            # Trigger video generation task
            task_id = task_service.start(
                "default",
                {
                    "subject": subject,
                    "platforms": platforms,
                    "video_source": video_source,
                },
            )

            return {
                "success": True,
                "task_id": task_id,
                "message": f"Video generation started for: {subject}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _publish_to_youtube(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle YouTube publishing request."""
        try:
            from app.services.upload_post import upload_post_service

            video_path = args.get("video_path", "")
            title = args.get("title", "")
            description = args.get("description", "")
            privacy_status = args.get("privacy_status", "public")
            tags = args.get("tags", [])

            if not video_path or not title:
                return {"success": False, "error": "video_path and title are required"}

            youtube_extra = {
                "youtube_title": title,
                "youtube_description": description,
                "tags": tags,
                "privacyStatus": privacy_status,
            }

            result = upload_post_service.upload_video(
                video_path,
                title,
                platforms=["youtube"],
                youtube_extra=youtube_extra,
            )

            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _get_youtube_channel_info(self) -> Dict[str, Any]:
        """Get YouTube channel information."""
        try:
            # This would integrate with YouTube API if configured
            return {
                "success": True,
                "channel": "orynx-00",
                "url": "https://youtube.com/@orynx-00",
                "message": "YouTube channel info retrieved",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _call_nexlev_tool(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Call a NexLev tool."""
        try:
            from app.services.nexlev import nexlev_service

            tool_name = args.get("tool_name", "")
            tool_arguments = args.get("arguments", {})

            if not tool_name:
                return {"success": False, "error": "tool_name is required"}

            return await nexlev_service.call_tool(tool_name, tool_arguments)
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _list_nexlev_tools(self) -> Dict[str, Any]:
        """List all NexLev tools."""
        try:
            from app.services.nexlev import nexlev_service

            return await nexlev_service.list_tools()
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _get_repository_info(self) -> Dict[str, Any]:
        """Get GitHub repository information."""
        try:
            from app.services.github import github_service

            return github_service.get_repo_info()
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _get_recent_commits(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get recent commits from the repository."""
        try:
            from app.services.github import github_service

            count = args.get("count", 10)
            return github_service.get_recent_commits(count)
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _create_github_issue(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a GitHub issue."""
        try:
            from app.services.github import github_service

            title = args.get("title", "")
            body = args.get("body", "")
            labels = args.get("labels", [])

            if not title:
                return {"success": False, "error": "title is required"}

            return github_service.create_issue(title, body, labels)
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _analyze_content_performance(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content performance metrics."""
        try:
            # Placeholder for content analysis
            return {
                "success": True,
                "analysis": {
                    "metrics_requested": args.get("metrics", []),
                    "status": "Analysis would run here",
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def run(self):
        """Run the MCP server with stdin/stdout transport."""
        logger.info("Starting MoneyPrintTurbo MCP Server...")

        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                data = json.loads(line)
                response = await self.process_request(data)
                print(json.dumps(response))
                sys.stdout.flush()

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                print(json.dumps({"error": "Invalid JSON"}))
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                print(json.dumps({"error": str(e)}))
                sys.stdout.flush()

    async def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process an incoming MCP request."""
        method = data.get("method", "")
        params = data.get("params", {})
        request_id = data.get("id", 1)

        try:
            if method == "tools/list":
                result = self.handle_tools_list()
            elif method == "tools/call":
                tool_name = params.get("name", "")
                tool_args = params.get("arguments", {})
                result = await self.handle_tools_call(tool_name, tool_args)
            else:
                result = {"error": f"Unknown method: {method}"}

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result,
            }
        except Exception as e:
            logger.error(f"Error processing {method}: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -1,
                    "message": str(e),
                },
            }


async def main():
    """Main entry point."""
    server = MCPServer()
    await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("MCP Server shutting down...")
        sys.exit(0)
