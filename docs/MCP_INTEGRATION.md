# MoneyPrintTurbo MCP Integration Guide

This guide explains how to connect Claude, YouTube, NexLev, and GitHub integrations to your MoneyPrintTurbo codebase for use with AI agents.

## Overview

The integration enables:
- **Claude**: AI-powered script generation and content analysis
- **YouTube**: Automated video publishing to your channel
- **NexLev**: Workflow automation and data management
- **GitHub**: Repository management and collaboration

## Prerequisites

1. **Claude API Key** - Get from https://console.anthropic.com/
2. **YouTube Upload-Post Account** - Register at https://upload-post.com/
3. **NexLev API Key** - Get from https://prod.dashboard.nexlev.io/
4. **GitHub Token** - Generate at https://github.com/settings/tokens

## Configuration Steps

### 1. Update config.toml

Edit `config.toml` and set your credentials:

```toml
# Claude LLM Provider
llm_provider = "anthropic"
anthropric_api_key = "your-claude-api-key-here"
anthropric_model_name = "claude-3-5-sonnet-20241022"

# YouTube Publishing
upload_post_enabled = true
upload_post_api_key = "your-upload-post-api-key"
upload_post_username = "your-upload-post-username"
upload_post_platforms = ["youtube", "tiktok", "instagram"]
upload_post_auto_upload = true
upload_post_youtube_privacy_status = "public"
upload_post_youtube_channel_id = "your-channel-id"

# NexLev Integration
nexlev_mcp_url = "https://prod.dashboard.nexlev.io/api/mcp"
nexlev_api_key = "your-nexlev-api-key"
```

### 2. Set Environment Variables

```bash
export GITHUB_TOKEN="your-github-token"
export ANTHROPIC_API_KEY="your-claude-api-key"
```

Or add to `.env` file:
```
GITHUB_TOKEN=your-github-token
ANTHROPIC_API_KEY=your-claude-api-key
```

### 3. Services Installed

The following services are now available:

#### app/services/nexlev.py
- `call_tool()` - Call NexLev MCP tools
- `list_tools()` - List available tools
- `automate_workflow()` - Trigger workflows
- `get_data()` - Retrieve data
- `store_data()` - Store data

#### app/services/github.py
- `get_repo_info()` - Get repository information
- `create_issue()` - Create GitHub issues
- `get_recent_commits()` - Retrieve commit history
- `get_workflows_status()` - Check workflow status

#### app/services/upload_post.py (Enhanced)
- `upload_video()` - Publish to YouTube/TikTok/Instagram
- Enhanced YouTube channel support

## Using the MCP Server

### Starting the MCP Server

```bash
cd /workspaces/MoneyPrintTurbo
python3 app/mcp_server.py
```

### Integrating with Claude in VS Code

#### Option 1: Direct MCP Configuration

Create or edit `~/.vscode/settings.json`:

```json
{
  "claude.extension.enableMCP": true,
  "claude.extension.mcpServers": {
    "moneyprinter": {
      "type": "stdio",
      "command": "python3",
      "args": ["/workspaces/MoneyPrintTurbo/app/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/workspaces/MoneyPrintTurbo"
      }
    }
  }
}
```

#### Option 2: Using Cursor or Claude Desktop Client

For Claude Desktop Client, edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "moneyprinter": {
      "type": "stdio",
      "command": "python3",
      "args": ["/workspaces/MoneyPrintTurbo/app/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/workspaces/MoneyPrintTurbo",
        "GITHUB_TOKEN": "your-token-here"
      }
    }
  }
}
```

## Available MCP Tools

Once configured, Claude can use these tools:

### Video Generation
- `generate_video(subject, platforms, video_source)` - Create and publish videos

### YouTube
- `publish_to_youtube(video_path, title, description, privacy_status, tags)` - Publish videos
- `get_youtube_channel_info()` - Get channel details

### NexLev
- `call_nexlev_tool(tool_name, arguments)` - Call any NexLev tool
- `list_nexlev_tools()` - List available NexLev tools

### GitHub
- `get_repository_info()` - Repository details
- `get_recent_commits(count)` - Recent commits
- `create_github_issue(title, body, labels)` - Create issues

### Analytics
- `analyze_content_performance(metrics)` - Analyze video performance

## Testing the Integration

### Test from Python

```python
from app.services.github import github_service
from app.services.nexlev import nexlev_service
from app.services.upload_post import upload_post_service

# Test GitHub
print(github_service.get_repo_info())

# Test NexLev (async)
import asyncio
result = asyncio.run(nexlev_service.call_tool("tool_name", {}))
print(result)

# Test Upload-Post
print(upload_post_service.is_configured())
```

### Test from CLI

```bash
# Start the MCP server
python3 app/mcp_server.py

# In another terminal, send a test request:
echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}' | python3 app/mcp_server.py
```

## File Structure

```
app/
├── mcp_server.py           # MCP server implementation
├── services/
│   ├── github.py           # GitHub integration
│   ├── nexlev.py           # NexLev MCP integration
│   ├── upload_post.py      # YouTube/TikTok publishing (enhanced)
│   └── ...
├── controllers/            # API endpoints
└── ...

config.toml                  # Configuration file
```

## Workflow Example

1. Claude analyzes your YouTube channel via GitHub
2. Generates video script using Claude LLM
3. Creates video using MoneyPrintTurbo
4. Publishes to YouTube via Upload-Post
5. Logs results in GitHub Issues
6. Triggers NexLev workflows for promotion

## Troubleshooting

### MCP Server won't start
- Check Python is in PATH: `which python3`
- Verify dependencies: `pip install -r requirements.txt`
- Check config.toml syntax

### Claude can't call tools
- Verify MCP server is running
- Check `.vscode/settings.json` or Claude desktop config
- Look for errors in VS Code's Output panel (MCP tab)

### API Credentials not working
- Double-check credentials in `config.toml`
- Verify environment variables are set
- Check API key permissions and expiry

### YouTube publishing fails
- Verify Upload-Post account is active
- Check API key is valid
- Ensure channel settings allow auto-publishing

## Security Notes

- **Never commit API keys** to version control
- Use environment variables for sensitive data
- Store credentials in `.env` files (add to `.gitignore`)
- Rotate tokens regularly
- Use channel-specific upload accounts if possible

## Next Steps

1. ✅ Configure `config.toml` with your credentials
2. ✅ Set environment variables
3. ✅ Start the MCP server
4. ✅ Connect Claude in VS Code or Claude Desktop
5. Ask Claude to help with:
   - Video generation and publishing
   - GitHub repository updates
   - NexLev workflow automation
   - Content analysis and optimization

## Support

For issues or questions:
- Check configuration in `config.toml`
- Review MCP server logs: `python3 app/mcp_server.py 2>&1 | grep -i error`
- Test individual services in Python REPL
- Review API documentation for each service

## References

- Claude API: https://docs.anthropic.com/
- Upload-Post: https://docs.upload-post.com/
- NexLev: https://prod.dashboard.nexlev.io/
- GitHub API: https://docs.github.com/en/rest
- MCP Specification: https://spec.modelcontextprotocol.io/
