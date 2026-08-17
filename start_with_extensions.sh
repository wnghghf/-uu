#!/bin/bash
# Start MoneyPrintTurbo with all Extensions as Model Sources
# This script starts both MCP servers needed for full Claude integration

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  MoneyPrintTurbo - Extensions as Model Sources            ║${NC}"
echo -e "${BLUE}║  Starting Claude Integration with IDE Tools              ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "config.toml" ]; then
    echo -e "${RED}✗ Not in MoneyPrintTurbo root directory${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Found MoneyPrintTurbo root${NC}"
echo ""

# Check if .env exists and has credentials
if [ -f ".env" ]; then
    echo -e "${YELLOW}→ Loading environment from .env${NC}"
    source .env
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 available${NC}"

# Create logs directory
mkdir -p logs
echo -e "${GREEN}✓ Logs directory ready${NC}"
echo ""

# Function to start a service
start_service() {
    local name=$1
    local cmd=$2
    local log_file=$3
    
    echo -e "${YELLOW}→ Starting $name...${NC}"
    $cmd > "$log_file" 2>&1 &
    local pid=$!
    
    # Wait a moment and check if process is still running
    sleep 2
    if ps -p $pid > /dev/null; then
        echo -e "${GREEN}✓ $name started (PID: $pid)${NC}"
        echo "$pid" > "logs/${name}.pid"
        return 0
    else
        echo -e "${RED}✗ $name failed to start${NC}"
        cat "$log_file"
        return 1
    fi
}

echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Starting MCP Servers${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo ""

# Start MoneyPrintTurbo server
start_service \
    "MoneyPrintTurbo MCP" \
    "python3 app/mcp_server.py" \
    "logs/moneyprinter.log" || {
    echo -e "${RED}Failed to start MoneyPrintTurbo MCP server${NC}"
    exit 1
}

echo ""

# Start Python Tools server
start_service \
    "Python Tools MCP" \
    "python3 run_python_tools.py" \
    "logs/python_tools.log" || {
    echo -e "${YELLOW}⚠ Python Tools MCP server failed (optional)${NC}"
}

echo ""
echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Extension Model Sources Status${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${GREEN}✓ Claude Code Extension       ${NC} (Direct Claude integration)"
echo -e "${GREEN}✓ Pylance                     ${NC} (Python type checking & analysis)"
echo -e "${GREEN}✓ Python Extension            ${NC} (Testing, debugging, linting)"
echo -e "${GREEN}✓ GitHub Integration          ${NC} (PRs, issues, commits)"
echo ""

echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}MCP Tools Available (17 total)${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}MoneyPrintTurbo Tools (9):${NC}"
echo "  ✓ generate_video            ✓ publish_to_youtube      ✓ get_youtube_channel_info"
echo "  ✓ call_nexlev_tool          ✓ list_nexlev_tools       ✓ get_repository_info"
echo "  ✓ get_recent_commits        ✓ create_github_issue     ✓ analyze_content_performance"
echo ""

echo -e "${YELLOW}Python Analysis Tools (8):${NC}"
echo "  ✓ analyze_code              ✓ get_type_hints          ✓ check_imports"
echo "  ✓ find_references           ✓ get_docstring           ✓ discover_tests"
echo "  ✓ check_code_quality        ✓ get_api_signature"
echo ""

echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Next Steps${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo ""

echo "1. Reload VS Code"
echo "   - Press Ctrl+Shift+P (or Cmd+Shift+P on Mac)"
echo "   - Type: Developer: Reload Window"
echo "   - Press Enter"
echo ""

echo "2. Verify Extensions Loaded"
echo "   - Check VS Code Extension panel"
echo "   - Ensure Claude Code is active"
echo "   - Check Pylance is analyzing code"
echo ""

echo "3. Check MCP Servers"
echo "   - View logs: tail -f logs/moneyprinter.log"
echo "   - Both servers should be waiting for JSON-RPC requests"
echo ""

echo "4. Start Asking Claude!"
echo "   Examples:"
echo "     → 'Generate a video about AI and publish it to YouTube'"
echo "     → 'Analyze this code for quality issues'"
echo "     → 'Create a GitHub issue for this feature'"
echo "     → 'Review the code in app/services/llm.py'"
echo ""

echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ MoneyPrintTurbo with Extensions Ready!${NC}"
echo -e "${BLUE}═════════════════════════════════════════════════════════════${NC}"
echo ""

echo "Servers running:"
echo "  - MoneyPrintTurbo MCP: http://localhost:8080 (internal)"
echo "  - Python Tools MCP: stdio transport"
echo ""

echo "To stop servers:"
echo "  kill \$(cat logs/*.pid)"
echo ""

echo "For more details, see:"
echo "  - EXTENSION_SOURCES.md"
echo "  - .vscode/copilot-instructions.md"
echo "  - docs/MCP_INTEGRATION.md"
echo ""

# Keep script running to show logs
echo -e "${YELLOW}Monitoring logs (Ctrl+C to stop)...${NC}"
echo ""

# Tail all logs
tail -f logs/*.log 2>/dev/null || wait
