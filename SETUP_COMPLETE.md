# MoneyPrintTurbo MCP Integration - Setup Complete! ✓

Your codebase is now fully configured to use Claude, YouTube, NexLev, and GitHub integrations through the Model Context Protocol (MCP).

## What Was Installed

### 1. **Configuration (config.toml)**
- ✅ Claude/Anthropic LLM provider configured
- ✅ YouTube Upload-Post enabled for video publishing
- ✅ NexLev MCP endpoint configured (https://prod.dashboard.nexlev.io/api/mcp)
- ✅ GitHub integration ready

### 2. **Services Created**
| Service | File | Purpose |
|---------|------|---------|
| **NexLev MCP** | `app/services/nexlev.py` | Call NexLev workflows and automation tools |
| **GitHub** | `app/services/github.py` | Repo management, issues, commits, workflows |
| **Upload-Post** (Enhanced) | `app/services/upload_post.py` | YouTube/TikTok/Instagram publishing |
| **MCP Server** | `app/mcp_server.py` | Exposes 9 tools for Claude to use |

### 3. **Tools Available to Claude (9 total)**
```
✓ generate_video              - Create videos from text
✓ publish_to_youtube          - Publish to YouTube
✓ get_youtube_channel_info    - Channel details
✓ call_nexlev_tool            - Call any NexLev tool
✓ list_nexlev_tools           - List available tools
✓ get_repository_info         - Repo details
✓ get_recent_commits          - Commit history
✓ create_github_issue         - Create issues
✓ analyze_content_performance - Performance analysis
```

### 4. **Documentation**
- 📖 `docs/MCP_INTEGRATION.md` - Comprehensive setup guide
- 🔧 `.vscode/mcp-settings-template.json` - VS Code config template
- 🔧 `.vscode/claude-desktop-config-template.json` - Claude Desktop template

### 5. **Utilities**
- 📝 `setup_mcp_integration.sh` - Interactive setup helper
- ✅ `verify_mcp_setup.py` - Verification & status checker

## Current Status

| Integration | Status | Notes |
|-------------|--------|-------|
| **GitHub** | ✅ Ready | Token already configured |
| **Claude** | 🔑 API Key needed | See below |
| **YouTube** | 🔑 API Key needed | See below |
| **NexLev** | 🔑 API Key needed | See below |

## What You Need to Do

### Step 1: Get Your API Keys

1. **Claude API**: https://console.anthropic.com/
   - Create account → API Keys → Create new key

2. **Upload-Post (YouTube)**: https://upload-post.com/
   - Create account → Get API key and username
   - Your channel: https://youtube.com/@orynx-00

3. **NexLev MCP**: https://prod.dashboard.nexlev.io/
   - Sign in → Get API key from dashboard

### Step 2: Update Configuration

Edit `config.toml` and fill in:
```toml
anthropric_api_key = "your-claude-api-key"
upload_post_api_key = "your-upload-post-key"
upload_post_username = "your-username"
nexlev_api_key = "your-nexlev-key"
```

Or use the interactive setup:
```bash
./setup_mcp_integration.sh
```

### Step 3: Set Environment Variables

Create or update `.env`:
```bash
export ANTHROPIC_API_KEY="your-key"
export GITHUB_TOKEN="your-token"  # Already set
export NEXLEV_API_KEY="your-key"
export UPLOAD_POST_API_KEY="your-key"
```

Then load it:
```bash
source .env
```

### Step 4: Verify Setup

Check everything is working:
```bash
python3 verify_mcp_setup.py
```

### Step 5: Start MCP Server

```bash
python3 app/mcp_server.py
```

### Step 6: Connect Claude

**Option A: VS Code with Copilot**
```bash
# Copy template to active config
cp .vscode/mcp-settings-template.json .vscode/settings.json

# Edit the path and environment variables
# Then restart VS Code
```

**Option B: Claude Desktop Client**
- On macOS: Update `~/Library/Application Support/Claude/claude_desktop_config.json`
- On Windows: Update `%APPDATA%\Claude\claude_desktop_config.json`
- Copy from: `.vscode/claude-desktop-config-template.json`

## Using It

Once configured, you can ask Claude to:

```
"Generate a video about [topic] and publish it to YouTube"
"Create a GitHub issue for [feature request]"
"List my recent commits"
"Check NexLev workflow status"
"Analyze video performance metrics"
```

## File Structure

```
MoneyPrintTurbo/
├── app/
│   ├── mcp_server.py           ← MCP server with 9 tools
│   ├── services/
│   │   ├── nexlev.py           ← NexLev integration
│   │   ├── github.py           ← GitHub integration
│   │   ├── upload_post.py      ← Enhanced YouTube support
│   │   └── ...
│   └── ...
├── config.toml                  ← Update with your keys
├── .env                         ← Environment variables
├── docs/
│   └── MCP_INTEGRATION.md      ← Full documentation
├── .vscode/
│   ├── mcp-settings-template.json
│   └── claude-desktop-config-template.json
├── setup_mcp_integration.sh     ← Setup helper
├── verify_mcp_setup.py          ← Status checker
└── ...
```

## Troubleshooting

### "MCP server won't start"
```bash
# Check Python
which python3

# Verify dependencies
pip install -r requirements.txt

# Check config syntax
python3 -c "from app.config import config; print('OK')"
```

### "Claude can't find tools"
- Ensure MCP server is running: `python3 app/mcp_server.py`
- Check `.vscode/settings.json` or Claude Desktop config
- Restart VS Code or Claude Desktop client

### "API calls failing"
- Verify API keys are correct
- Check they have proper permissions
- Ensure tokens aren't expired
- Run `python3 verify_mcp_setup.py` for diagnostics

## Next Steps

1. ✅ Get your API keys from the services listed above
2. ✅ Run `./setup_mcp_integration.sh` or manually update `config.toml`
3. ✅ Run `python3 verify_mcp_setup.py` to verify
4. ✅ Start MCP server: `python3 app/mcp_server.py`
5. ✅ Connect Claude (VS Code or Desktop)
6. ✅ Start asking Claude to help! 🎉

## Documentation

- Full setup guide: [docs/MCP_INTEGRATION.md](docs/MCP_INTEGRATION.md)
- Service implementations:
  - [app/services/nexlev.py](app/services/nexlev.py)
  - [app/services/github.py](app/services/github.py)
  - [app/mcp_server.py](app/mcp_server.py)

## Security Notes

⚠️ **IMPORTANT**
- Never commit API keys to Git
- Use environment variables for sensitive data
- Add `.env` to `.gitignore` (usually already done)
- Rotate tokens regularly
- Use dedicated API keys for this integration

## Support

For issues:
1. Check `docs/MCP_INTEGRATION.md` for detailed docs
2. Run `verify_mcp_setup.py` for diagnostics
3. Review logs: `python3 app/mcp_server.py 2>&1 | tail -20`
4. Test services individually in Python REPL

---

**You're all set!** Your MoneyPrintTurbo codebase is now ready to work with Claude, YouTube, NexLev, and GitHub. Just add your API keys and start building! 🚀
