#!/usr/bin/env python3
"""
Quick start verification and testing script for MoneyPrintTurbo MCP integrations.
This script tests all integrations to ensure they are properly configured.
"""

import sys
import os
import json
import asyncio
from pathlib import Path

# Add the repo to path
sys.path.insert(0, '/workspaces/MoneyPrintTurbo')

from loguru import logger
from app.config import config
from app.services.github import github_service
from app.services.nexlev import nexlev_service
from app.services.upload_post import upload_post_service
from app.mcp_server import MCPServer


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_status(name, configured, message=""):
    """Print status of a service."""
    status = "✓ READY" if configured else "✗ NOT CONFIGURED"
    symbol = "✓" if configured else "✗"
    print(f"  {symbol} {name:<25} {status:<15} {message}")


def test_claude():
    """Test Claude/LLM configuration."""
    print_header("CLAUDE LLM PROVIDER")
    
    llm_provider = config.app.get("llm_provider", "")
    anthropic_key = config.app.get("anthropric_api_key", "")
    
    configured = llm_provider == "anthropic" and bool(anthropic_key)
    print_status("Claude", configured)
    print(f"  Provider: {llm_provider}")
    print(f"  Model: {config.app.get('anthropric_model_name', 'Not set')}")
    print(f"  API Key: {'Set' if anthropic_key else 'Not set'}")
    
    return configured


def test_youtube():
    """Test YouTube Upload-Post configuration."""
    print_header("YOUTUBE PUBLISHING")
    
    configured = upload_post_service.is_configured()
    print_status("YouTube Upload-Post", configured)
    print(f"  Enabled: {config.app.get('upload_post_enabled', False)}")
    print(f"  Platforms: {config.app.get('upload_post_platforms', [])}")
    print(f"  API Key: {'Set' if upload_post_service.api_key else 'Not set'}")
    print(f"  Username: {upload_post_service.username if upload_post_service.username else 'Not set'}")
    print(f"  Channel: https://youtube.com/@orynx-00")
    
    return configured


def test_nexlev():
    """Test NexLev MCP configuration."""
    print_header("NEXLEV MCP")
    
    configured = nexlev_service.enabled
    print_status("NexLev", configured)
    print(f"  MCP URL: {nexlev_service.mcp_url}")
    print(f"  API Key: {'Set' if nexlev_service.api_key else 'Not set'}")
    print(f"  Enabled: {configured}")
    
    return configured


def test_github():
    """Test GitHub integration configuration."""
    print_header("GITHUB INTEGRATION")
    
    configured = github_service.is_configured()
    print_status("GitHub", configured)
    print(f"  Repository: {github_service.github_repo}")
    print(f"  Token: {'Set' if github_service.github_token else 'Not set'}")
    print(f"  Enabled: {configured}")
    
    return configured


def test_mcp_server():
    """Test MCP server registration."""
    print_header("MCP SERVER")
    
    try:
        server = MCPServer()
        tools = server.handle_tools_list()
        tool_count = len(tools.get("tools", []))
        
        print(f"  ✓ MCP Server initialized")
        print(f"  ✓ {tool_count} tools registered\n")
        
        print("  Available tools:")
        for tool in tools.get("tools", []):
            print(f"    - {tool['name']:<30} {tool['description']}")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


async def test_services():
    """Test actual service functionality."""
    print_header("SERVICE CONNECTIVITY TEST")
    
    # Test GitHub
    if github_service.is_configured():
        print("\n  Testing GitHub service...")
        result = github_service.get_repo_info()
        if result.get("success"):
            print(f"    ✓ Connected to: {result.get('name')}")
        else:
            print(f"    ✗ Failed: {result.get('error')}")
    
    # Test NexLev
    if nexlev_service.enabled:
        print("\n  Testing NexLev service...")
        result = await nexlev_service.list_tools()
        if result.get("success"):
            print(f"    ✓ Found {len(result.get('tools', []))} NexLev tools")
        else:
            print(f"    ℹ Note: {result.get('error', 'Connection test skipped')}")
    
    # Test Upload-Post
    if upload_post_service.is_configured():
        print("\n  Testing Upload-Post service...")
        print(f"    ✓ Upload-Post configured and ready")


def print_next_steps():
    """Print next steps for the user."""
    print_header("NEXT STEPS")
    
    print("""
1. CONFIGURE CREDENTIALS
   ─────────────────────────
   Edit config.toml and add your API keys:
   
   ➤ Claude API: https://console.anthropic.com/
   ➤ Upload-Post: https://upload-post.com/
   ➤ NexLev MCP: https://prod.dashboard.nexlev.io/
   ➤ GitHub Token: https://github.com/settings/tokens

2. SET ENVIRONMENT VARIABLES
   ──────────────────────────
   source .env
   
   Or set them in your shell:
   export ANTHROPIC_API_KEY="your-key"
   export GITHUB_TOKEN="your-token"

3. START MCP SERVER
   ─────────────────
   python3 app/mcp_server.py

4. CONNECT CLAUDE
   ───────────────
   Option A: VS Code + Copilot
   - Copy .vscode/mcp-settings-template.json to .vscode/settings.json
   - Restart VS Code
   
   Option B: Claude Desktop Client
   - Copy .vscode/claude-desktop-config-template.json
   - Update ~/Library/Application\\ Support/Claude/claude_desktop_config.json (macOS)
   - or %APPDATA%\\Claude\\claude_desktop_config.json (Windows)

5. START USING!
   ─────────────
   Ask Claude to:
   - Generate videos from scripts
   - Publish to YouTube
   - Trigger NexLev workflows
   - Manage GitHub issues
   - Analyze content performance

For more info, see: docs/MCP_INTEGRATION.md
    """)


def main():
    """Main verification script."""
    print("""
╔════════════════════════════════════════════════════════════╗
║  MoneyPrintTurbo MCP Integration Verification              ║
║  Claude + YouTube + NexLev + GitHub                        ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    results = {
        "Claude": test_claude(),
        "YouTube": test_youtube(),
        "NexLev": test_nexlev(),
        "GitHub": test_github(),
        "MCP Server": test_mcp_server(),
    }
    
    # Test services async
    print_header("CONNECTIVITY TESTS")
    try:
        asyncio.run(test_services())
    except Exception as e:
        print(f"  Note: Service connectivity tests require running server")
    
    # Summary
    print_header("CONFIGURATION SUMMARY")
    configured_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    print(f"  Configured: {configured_count}/{total_count} services\n")
    
    if configured_count == total_count:
        print("  🎉 All integrations are ready to use!")
    elif configured_count > 0:
        print("  ✓ Some integrations are ready!")
        print("  ℹ Configure remaining services for full functionality")
    else:
        print("  ℹ No integrations configured yet")
        print("  Follow the next steps to get started")
    
    print_next_steps()
    
    return 0 if configured_count > 0 else 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
