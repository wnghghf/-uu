# Extension Model Sources Setup Guide

Your MoneyPrintTurbo workspace is now configured to use installed VS Code extensions as intelligent model sources for Claude. This enables advanced code analysis, type checking, and IDE-aware code generation.

## What's Installed & Configured

### Extensions Available
| Extension | Purpose | Status |
|-----------|---------|--------|
| **Claude Code** | Direct Claude integration | ✅ Enabled |
| **Pylance** | Python type checking & analysis | ✅ Active |
| **Python** | Testing, debugging, linting | ✅ Ready |
| **GitHub** | PR management, issues, commits | ✅ Configured |
| **Sixth AI** | Alternative AI capabilities | ✅ Available |

### Model Sources Configured

#### 1. **Claude Code Extension**
- Enabled: Inline completions, auto-suggestions
- Default Model: `claude-3-5-sonnet-20241022`
- Fallback Models: `claude-opus-4-1`, `claude-3-haiku-20240307`
- MCP Integration: ✅ Enabled

#### 2. **Pylance (Python IntelliSense)**
- Analysis Mode: `standard`
- Type Checking: Workspace-level
- Features:
  - Type inference and validation
  - Import optimization
  - Symbol reference finding
  - Code quality metrics

#### 3. **GitHub Integration**
- Authentication: Token-based
- Repository: BrunoLuke-creator/MoneyPrintTurbo
- Capabilities:
  - View PRs and issues
  - Manage commits
  - Check workflow status

#### 4. **Python Extension**
- Testing: Test discovery & execution
- Debugging: Interactive debugging
- Linting: pylint enabled
- Formatting: Auto-format on save

## MCP Tools Now Available (17 total)

### MoneyPrintTurbo Tools (9 tools)
```
✓ generate_video              → Create videos
✓ publish_to_youtube          → Publish to YouTube
✓ get_youtube_channel_info    → Channel info
✓ call_nexlev_tool            → Trigger automation
✓ list_nexlev_tools           → List tools
✓ get_repository_info         → GitHub repo info
✓ get_recent_commits          → Commit history
✓ create_github_issue         → Create issues
✓ analyze_content_performance → Video metrics
```

### Python Analysis Tools (8 tools)
```
✓ analyze_code                → Find errors/warnings
✓ get_type_hints              → Type inference
✓ check_imports               → Import validation
✓ find_references             → Symbol usage
✓ get_docstring               → Extract docs
✓ discover_tests              → Find tests
✓ check_code_quality          → Quality metrics
✓ get_api_signature           → Function signatures
```

## Configuration Files

### `.vscode/settings.json` ✅ Created
- Enables Claude Code extension
- Configures Pylance analysis
- Sets up GitHub authentication
- Registers MCP servers
- Auto-save and formatting options

### `.vscode/copilot-instructions.md` ✅ Created
- Comprehensive guide for Claude
- How to use each extension
- Example prompts and workflows
- Troubleshooting tips

### `.vscode/mcp-settings-template.json` ✅ Ready
- Template for MCP server configuration
- Environment variable mappings
- User-ready configuration

### `extension-tools/python_tools.py` ✅ Created
- Pylance integration server
- Code analysis capabilities
- Python tooling MCP server

## Quick Start

### 1. Verify Extensions Are Installed
```bash
code --list-extensions
# Should show:
# - anthropic.claude-code
# - ms-python.vscode-pylance
# - ms-python.python
# - github.vscode-pull-request-github
```

### 2. Start MCP Servers
```bash
# Terminal 1: MoneyPrintTurbo tools
python3 app/mcp_server.py

# Terminal 2: Python analysis tools
python3 extension-tools/python_tools.py
```

### 3. Set Environment Variables
```bash
source .env
```

Or:
```bash
export ANTHROPIC_API_KEY="your-key"
export GITHUB_TOKEN="your-token"
export NEXLEV_API_KEY="your-key"
export UPLOAD_POST_API_KEY="your-key"
```

### 4. Reload VS Code
- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
- Type "Developer: Reload Window"
- Press Enter

### 5. Start Using!
Ask Claude questions like:
```
"Generate a video about Python best practices"
"Analyze this code for issues"
"Create a GitHub issue for this feature"
"Publish my latest video to YouTube"
```

## How Claude Uses Each Extension

### Claude Code Extension
Claude sees inline completions and auto-suggestions, enabling:
- Code generation in context
- Real-time refactoring suggestions
- Error highlighting

### Pylance
Claude leverages type information to:
- Generate type-safe code
- Understand code structure
- Find potential bugs before runtime
- Suggest correct API usage

### Python Extension
Claude uses testing and debugging capabilities to:
- Discover and run tests
- Understand code flow
- Validate implementations
- Debug failing tests

### GitHub Integration
Claude accesses repository context:
- Understand code history
- Reference recent changes
- Create tracking issues
- Check workflow status

## Example Workflows

### 1. Intelligent Code Generation
```
User: "Generate a service for handling video uploads with proper error handling"
Claude:
→ Analyzes existing services with Pylance
→ Uses type hints to match code style
→ Generates type-safe implementation
→ Suggests where tests should go
```

### 2. Full Feature Implementation
```
User: "Add support for Instagram Reels publishing"
Claude:
→ Examines existing YouTube/TikTok integration
→ Uses Python tools to find similar patterns
→ Generates Instagram implementation
→ Creates GitHub issue to track progress
→ Runs tests to validate
```

### 3. Video Generation Pipeline
```
User: "Generate a video about AI and publish it"
Claude:
→ Uses moneyprinter generate_video tool
→ Monitors progress
→ Publishes using publish_to_youtube tool
→ Creates GitHub issue as documentation
→ Triggers NexLev workflow for promotion
```

### 4. Code Review & Improvement
```
User: "Review app/services/llm.py and suggest improvements"
Claude:
→ Uses Pylance to analyze code
→ Finds unused imports (check_imports)
→ Identifies complexity issues (check_code_quality)
→ Suggests refactoring
→ Generates improved version
```

## Configuration Details

### VS Code Settings (`.vscode/settings.json`)

**Claude Code**:
```json
"claude.extension.enableMCP": true,
"claude.extension.enabled": true,
"claude.extension.inlineCompletions": true
```

**Pylance**:
```json
"pylance.analysis.typeCheckingMode": "standard",
"pylance.analysis.diagnosticMode": "workspace",
"python.analysis.extraPaths": ["${workspaceFolder}/app"]
```

**MCP Servers**:
```json
"claude.extension.mcpServers": {
  "moneyprinter": {
    "type": "stdio",
    "command": "python3",
    "args": ["/workspaces/MoneyPrintTurbo/app/mcp_server.py"]
  }
}
```

### Environment Variables

```bash
# .env file (add to .gitignore)
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."
export NEXLEV_API_KEY="..."
export UPLOAD_POST_API_KEY="..."
```

## Testing the Setup

### Verify All Extensions
```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '/workspaces/MoneyPrintTurbo')

from app.mcp_server import MCPServer
from extension_tools.python_tools import PythonToolsServer

# Test MoneyPrintTurbo server
mpt = MCPServer()
mpt_tools = mpt.handle_tools_list()
print(f"✓ MoneyPrintTurbo: {len(mpt_tools['tools'])} tools")

# Test Python tools server
python_tools = PythonToolsServer()
py_tools = python_tools.handle_tools_list()
print(f"✓ Python Tools: {len(py_tools['tools'])} tools")

print(f"\nTotal: {len(mpt_tools['tools']) + len(py_tools['tools'])} tools available")
EOF
```

### Test Pylance Integration
```bash
# Open app/services/llm.py in VS Code
# Pylance should show type information in hover tooltips
# This indicates Pylance is active and working
```

### Test GitHub Integration
```bash
# Try running the Python command:
python3 -c "from app.services.github import github_service; print(github_service.get_repo_info())"
# Should return: ✓ Connected to: MoneyPrintTurbo
```

## Tips for Best Results

1. **Keep Pylance Running**: The more type information available, the better Claude's suggestions
2. **Use Type Hints**: Claude generates better code when it understands types
3. **Leverage GitHub Context**: Reference commits and issues for better context
4. **Chain MCP Calls**: Use multiple tools in sequence for complex workflows
5. **Start Simple**: Try basic tasks first, then combine tools

## File Structure

```
MoneyPrintTurbo/
├── .vscode/
│   ├── settings.json                    ← Extension configuration
│   ├── copilot-instructions.md          ← Claude instructions
│   ├── mcp-settings-template.json       ← MCP config template
│   └── claude-desktop-config-template.json
├── extension-tools/
│   └── python_tools.py                  ← Python analysis MCP server
├── app/
│   ├── mcp_server.py                    ← MoneyPrintTurbo MCP server
│   ├── services/
│   │   ├── github.py                    ← GitHub integration
│   │   ├── nexlev.py                    ← NexLev integration
│   │   └── ...
│   └── ...
└── ...
```

## Troubleshooting

### Extensions Not Showing Up
1. Check `.vscode/settings.json` is valid JSON
2. Restart VS Code: `Cmd+Shift+P` → "Reload Window"
3. Verify extension IDs in settings match installed extensions

### Pylance Not Analyzing Code
1. Wait 10-15 seconds for background analysis
2. Check "Output" panel → "Python" for errors
3. Verify Python interpreter is set: `.vscode/settings.json` → `python.defaultInterpreterPath`

### Claude Can't Access Tools
1. Ensure MCP servers are running
2. Check console for errors: `python3 app/mcp_server.py`
3. Verify `GITHUB_TOKEN` and API keys are set

### Type Hints Not Working
1. Add type hints to your code (Claude will follow your style)
2. Check Python version is 3.8+ (required for type hints)
3. Add `py.typed` marker if creating packages

## Next Steps

1. ✅ Verify extensions are installed
2. ✅ Start MCP servers
3. ✅ Set environment variables
4. ✅ Reload VS Code
5. ✅ Read `.vscode/copilot-instructions.md`
6. ✅ Start asking Claude for help!

## Support

- **VS Code Extension Docs**: https://code.visualstudio.com/docs/editor/settings
- **Pylance Docs**: https://github.com/microsoft/pylance-release
- **Claude API Docs**: https://docs.anthropic.com/
- **MCP Spec**: https://spec.modelcontextprotocol.io/

---

**You're all set!** Your extensions are now intelligent model sources for Claude, providing type checking, code analysis, and repository context to enhance code generation and understanding.
