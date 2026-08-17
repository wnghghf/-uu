# Sixth AI Integration Setup Guide

✅ **Sixth AI is now fully integrated with MoneyPrintTurbo!**

## What's Configured

Your Sixth AI extension now has access to:

### 1. **All MoneyPrintTurbo MCP Tools** (9 tools)
- `generate_video` - Create videos from text
- `publish_to_youtube` - Publish to YouTube channel
- `get_youtube_channel_info` - Get channel statistics
- `call_nexlev_tool` - Trigger NexLev workflows
- `list_nexlev_tools` - List available NexLev tools
- `get_repository_info` - Get GitHub repo info
- `get_recent_commits` - Get commit history
- `create_github_issue` - Create GitHub issues
- `analyze_content_performance` - Analyze video performance

### 2. **All Python Analysis Tools** (8 tools)
- `analyze_code` - Find errors and warnings
- `get_type_hints` - Infer types and missing hints
- `check_imports` - Validate and optimize imports
- `find_references` - Locate symbol usage
- `get_docstring` - Extract documentation
- `discover_tests` - Find test cases
- `check_code_quality` - Measure complexity
- `get_api_signature` - Get function signatures

### 3. **GitHub Integration**
- Full access to GitHub repository via your authorized token
- Can create issues, view PRs, check commits
- Authentication: GitHub token-based

## Authentication Setup

### GitHub Authorization ✅
Since you've already authorized Sixth AI on GitHub:
1. Sixth AI has access to the BrunoLuke-creator/MoneyPrintTurbo repository
2. Your GITHUB_TOKEN is configured in `.vscode/settings.json`
3. All GitHub tools are automatically available

### Environment Variables Required

Make sure these are set in your terminal:
```bash
export GITHUB_TOKEN="your-github-token-here"
export ANTHROPIC_API_KEY="your-claude-api-key-here"  # If using Claude
```

To verify they're set:
```bash
echo $GITHUB_TOKEN
echo $ANTHROPIC_API_KEY
```

## Starting the MCP Servers

For Sixth AI to access the tools, the MCP servers must be running.

### Option 1: Automated (Recommended)
```bash
./start_with_extensions.sh
```

### Option 2: Manual
```bash
# Terminal 1
python3 app/mcp_server.py

# Terminal 2
python3 run_python_tools.py
```

## Using Sixth AI

Open the Sixth AI chat panel in VS Code and ask it to:

### Generate and Publish Videos
```
"Generate a short video about Python best practices and publish it to YouTube"
```

### Analyze GitHub Repository
```
"What are the recent commits in the repository?"
```

### Create GitHub Issues
```
"Create a GitHub issue for implementing a new video filter feature"
```

### Check Channel Performance
```
"Get my YouTube channel info and video performance metrics"
```

### Run NexLev Workflows
```
"List all available NexLev tools and run the promotion workflow"
```

### Code Analysis
```
"Analyze app/services/llm.py for code quality issues"
```

### Full Workflow
```
"Generate a video about AI trends, publish it to YouTube, and create a GitHub issue to track it"
```

## Configuration Files

### `.vscode/settings.json`
- Enables Sixth AI MCP support
- Configures MCP server connections
- Sets GitHub authentication mode
- Points to moneyprinter and python-tools servers

### `.vscode/copilot-instructions.md`
- Comprehensive guide for all available tools
- Example use cases
- Troubleshooting tips

## Troubleshooting

### MCP Servers Not Connecting
1. Verify Python is installed: `python3 --version`
2. Check server is running: `lsof -i :8000`
3. Start manually if needed:
   ```bash
   python3 app/mcp_server.py
   python3 run_python_tools.py
   ```

### GitHub Token Issues
1. Check token is set: `echo $GITHUB_TOKEN`
2. Verify token has repo access at https://github.com/settings/tokens
3. Token should have: `repo`, `workflow`, `read:user` scopes

### Tools Not Appearing
1. Reload VS Code: `Ctrl+R` (Cmd+R on Mac)
2. Check Sixth AI extension is enabled in settings
3. Verify MCP servers are running
4. Check `.vscode/settings.json` for correct paths

## Next Steps

1. ✅ Verify environment variables are set
2. ✅ Start MCP servers: `./start_with_extensions.sh`
3. ✅ Open Sixth AI chat in VS Code
4. ✅ Try a simple command first: `"Get my GitHub repository info"`
5. ✅ Then try more complex workflows

## Support

For issues with:
- **Sixth AI Extension**: Check VS Code extensions marketplace
- **GitHub Integration**: https://github.com/settings/tokens
- **MCP Servers**: See `docs/MCP_INTEGRATION.md`
- **MoneyPrintTurbo Tools**: See `README.md`

Happy automating! 🚀
