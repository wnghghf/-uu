#!/bin/bash
# MoneyPrintTurbo MCP Integration Setup Helper
# This script guides you through setting up Claude, YouTube, NexLev, and GitHub integrations

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  MoneyPrintTurbo MCP Integration Setup                     ║${NC}"
echo -e "${BLUE}║  Connect Claude, YouTube, NexLev & GitHub                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if config.toml exists
if [ ! -f "config.toml" ]; then
    echo -e "${RED}✗ config.toml not found in current directory${NC}"
    echo "  Please run this script from the MoneyPrintTurbo root directory"
    exit 1
fi

echo -e "${GREEN}✓ Found config.toml${NC}"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file for sensitive credentials..."
    cat > .env << 'EOF'
# API Keys - Add your credentials here (don't commit to Git!)
# These values will override config.toml entries

# Claude API
export ANTHROPIC_API_KEY=""

# GitHub
export GITHUB_TOKEN=""

# NexLev
export NEXLEV_API_KEY=""

# Upload-Post
export UPLOAD_POST_API_KEY=""
EOF
    echo -e "${GREEN}✓ Created .env file${NC}"
else
    echo -e "${YELLOW}→ .env file already exists${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}STEP 1: Get Your API Keys${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}1. Claude API Key${NC}"
echo "   URL: https://console.anthropic.com/"
echo "   - Sign in or create an account"
echo "   - Go to API Keys section"
echo "   - Create a new API key"
echo ""

echo -e "${YELLOW}2. Upload-Post (YouTube Publishing)${NC}"
echo "   URL: https://upload-post.com/"
echo "   - Create an account"
echo "   - Get your API key and username"
echo "   - Your YouTube channel: https://youtube.com/@orynx-00"
echo ""

echo -e "${YELLOW}3. NexLev MCP${NC}"
echo "   URL: https://prod.dashboard.nexlev.io/"
echo "   - Sign in to your dashboard"
echo "   - Get your API key"
echo "   - MCP endpoint: https://prod.dashboard.nexlev.io/api/mcp"
echo ""

echo -e "${YELLOW}4. GitHub Personal Access Token${NC}"
echo "   URL: https://github.com/settings/tokens"
echo "   - Create new token (classic)"
echo "   - Scopes: repo, workflow (if using Actions)"
echo ""

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}STEP 2: Update Configuration${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo "Option A: Interactive Setup (Recommended)"
echo "---"
read -p "Enter your Claude API Key (or press Enter to skip): " claude_key
if [ ! -z "$claude_key" ]; then
    sed -i "s/anthropric_api_key = \"\"/anthropric_api_key = \"$claude_key\"/" config.toml
    echo -e "${GREEN}✓ Claude API key configured${NC}"
fi

read -p "Enter your Upload-Post API Key: " upload_key
if [ ! -z "$upload_key" ]; then
    sed -i "s/upload_post_api_key = \"\"/upload_post_api_key = \"$upload_key\"/" config.toml
    echo -e "${GREEN}✓ Upload-Post API key configured${NC}"
fi

read -p "Enter your Upload-Post Username: " upload_user
if [ ! -z "$upload_user" ]; then
    sed -i "s/upload_post_username = \"\"/upload_post_username = \"$upload_user\"/" config.toml
    echo -e "${GREEN}✓ Upload-Post username configured${NC}"
fi

read -p "Enter your NexLev API Key: " nexlev_key
if [ ! -z "$nexlev_key" ]; then
    sed -i "s/nexlev_api_key = \"\"/nexlev_api_key = \"$nexlev_key\"/" config.toml
    echo -e "${GREEN}✓ NexLev API key configured${NC}"
fi

echo ""
echo "Option B: Manual Setup"
echo "---"
echo "Edit config.toml and update these fields:"
echo "  - anthropric_api_key"
echo "  - upload_post_api_key"
echo "  - upload_post_username"
echo "  - nexlev_api_key"
echo ""

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}STEP 3: Set Environment Variables${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

read -p "Enter your GitHub Personal Access Token: " github_token
if [ ! -z "$github_token" ]; then
    export GITHUB_TOKEN="$github_token"
    sed -i "s/export GITHUB_TOKEN=\"\"/export GITHUB_TOKEN=\"$github_token\"/" .env
    echo -e "${GREEN}✓ GitHub token configured in .env${NC}"
fi

echo ""
echo "Source the .env file to load environment variables:"
echo "  source .env"
echo ""

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}STEP 4: Verify Configuration${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

python3 << 'PYTHON_SCRIPT'
import sys
sys.path.insert(0, '/workspaces/MoneyPrintTurbo')

from app.services.github import github_service
from app.services.nexlev import nexlev_service
from app.services.upload_post import upload_post_service
from app.config import config

print("Configuration Status:")
print("─" * 50)

llm_provider = config.app.get("llm_provider", "")
print(f"LLM Provider: {llm_provider} {'✓' if llm_provider == 'anthropic' else '✗'}")

upload_enabled = config.app.get("upload_post_enabled", False)
upload_configured = upload_post_service.is_configured()
print(f"Upload-Post: {'✓ Configured' if upload_configured else '✗ Not configured'}")

nexlev_configured = nexlev_service.enabled
print(f"NexLev MCP: {'✓ Configured' if nexlev_configured else '✗ Not configured'}")

github_configured = github_service.is_configured()
print(f"GitHub: {'✓ Configured' if github_configured else '✗ Not configured'}")

print("─" * 50)
if github_configured or upload_configured or nexlev_configured:
    print("✓ At least one integration is ready!")
else:
    print("✗ Please configure at least one integration")

PYTHON_SCRIPT

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}STEP 5: Start Using the Integrations${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo "A. Start the MCP Server (for Claude integration):"
echo "   python3 app/mcp_server.py"
echo ""

echo "B. Using in Python:"
echo "   from app.services.github import github_service"
echo "   from app.services.nexlev import nexlev_service"
echo "   from app.services.upload_post import upload_post_service"
echo ""

echo "C. Using with Claude (VS Code):"
echo "   1. Ensure MCP server is running"
echo "   2. Claude will automatically discover available tools"
echo "   3. Ask Claude to help with video generation or publishing"
echo ""

echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo "Next steps:"
echo "1. Review your credentials in config.toml"
echo "2. Source the .env file: source .env"
echo "3. Start the MCP server: python3 app/mcp_server.py"
echo "4. Open Claude and ask it to help generate videos!"
echo ""

echo "For detailed documentation, see:"
echo "  docs/MCP_INTEGRATION.md"
echo ""
