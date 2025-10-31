# MCP Debugpy Demo

This repository demonstrates using [mcp-debugpy](https://github.com/markomanninen/mcp-debugpy) to debug a Python application with an intentional bug using AI agents through the Model Context Protocol (MCP).

## What's the Bug?

The `shopping_cart.py` application has a subtle bug in the `calculate_total()` method. When applying a discount:

- **Expected behavior**: A 10% discount on $100 should give $90
- **Actual behavior**: The calculation multiplies incorrectly, giving $10 instead!

The bug is on line 45 of `shopping_cart.py`:
```python
return subtotal * discount_amount  # BUG: Should subtract discount, not multiply!
```

## Prerequisites

- Python 3.8 or higher
- VS Code with the MCP extension (or Claude Desktop with MCP support)
- Git

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/YOUR_USERNAME/mcp-debugpy-demo.git
cd mcp-debugpy-demo

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install pytest

# Install mcp-debugpy from source (until published to PyPI)
pip install git+https://github.com/markomanninen/mcp-debugpy.git
```

### 2. Run the Tests (See the Bug!)

```bash
pytest test_shopping_cart.py -v
```

You'll see test failures showing the discount calculation is wrong:

```
FAILED test_shopping_cart.py::test_calculate_total_with_discount
FAILED test_shopping_cart.py::test_complex_scenario
```

### 3. Run the Application

```bash
python shopping_cart.py
```

Output will show:
```
Items in cart: 4
Subtotal: $1139.96
Total with 10% discount: $11.40
Expected total: $1025.96
WARNING: Total doesn't match expected value!
```

Notice how the total with discount ($11.40) is way off from the expected value ($1025.96)!

## Debugging with MCP Debugpy

**IMPORTANT**: After installation, you need to configure your MCP client (VS Code or Claude Desktop) to use the mcp-debugpy server.

### Option A: VS Code with MCP Extension

#### Step 1: Open in VS Code
```bash
cd mcp-debugpy-demo
code .
```

#### Step 2: Configure MCP Server
The repository includes `.vscode/settings.json` pre-configured. It uses the `mcp-debug-server` command that was installed by pip.

**What it looks like**:
```json
{
  "mcp.servers.agentDebug": {
    "command": "${workspaceFolder}/.venv/bin/mcp-debug-server",
    "cwd": "${workspaceFolder}"
  }
}
```

#### Step 3: Reload VS Code
- Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
- Type "Developer: Reload Window"
- Press Enter

#### Step 4: Verify MCP Server
- Open the AI chat panel
- You should see "agentDebug" server available
- Try asking: "What MCP tools are available?"

#### Step 5: Start Debugging
Ask the AI: **"Debug the shopping_cart.py bug using breakpoints"**

The AI agent can use these MCP tools:
- `dap_launch` - Start debugging with breakpoints
- `dap_locals` - Inspect variable values
- `dap_step_over` / `dap_step_in` - Step through code
- `dap_continue` - Continue execution
- `run_tests_json` - Run tests and analyze failures

### Option B: Claude Desktop

#### Step 1: Find Config File

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Step 2: Add MCP Server Configuration

Edit the config file and add (replace `/absolute/path/to/` with your actual path):

```json
{
  "mcpServers": {
    "agentDebug": {
      "command": "/absolute/path/to/mcp-debugpy-demo/.venv/bin/mcp-debug-server",
      "cwd": "/absolute/path/to/mcp-debugpy-demo"
    }
  }
}
```

**To get your absolute path**:
```bash
cd mcp-debugpy-demo
pwd
# Copy this path and use it above
```

#### Step 3: Restart Claude Desktop

Completely quit and relaunch Claude Desktop.

#### Step 4: Verify MCP Server

In a new conversation, ask: **"What MCP tools do you have available?"**

You should see tools like `dap_launch`, `dap_locals`, `run_tests_json`, etc.

#### Step 5: Start Debugging

Ask: **"Help me debug the shopping cart discount bug"**

### Option C: Claude Code (VS Code Extension)

Claude Code automatically detects the `.vscode/settings.json` configuration. Just:

1. Open the folder in VS Code
2. Make sure Claude Code extension is installed
3. Open Claude Code chat
4. Ask: **"Debug shopping_cart.py using breakpoints"**

### Troubleshooting MCP Setup

#### "mcp-debug-server: command not found"

The virtual environment isn't activated or mcp-debugpy isn't installed:
```bash
source .venv/bin/activate
pip install git+https://github.com/markomanninen/mcp-debugpy.git
which mcp-debug-server  # Should show path in .venv/bin/
```

#### "MCP server not connecting"

1. Check the path in settings is correct (absolute paths work best)
2. Make sure the virtual environment exists
3. Try running the server manually to see errors:
   ```bash
   .venv/bin/mcp-debug-server --help
   ```

#### "No MCP tools available"

1. Reload VS Code window (Cmd/Ctrl+Shift+P → "Developer: Reload Window")
2. Check VS Code Output panel for MCP server errors
3. Verify the MCP extension is installed and enabled

### Manual Configuration (Alternative)

If you prefer not to use the pre-configured `.vscode/settings.json`, you can configure manually:

1. Open VS Code Settings (JSON)
2. Add the MCP server configuration manually
3. Use absolute paths for reliability



## The Fix

Once you've identified the bug on line 45, the fix is simple:

```python
# WRONG (current):
return subtotal * discount_amount

# CORRECT:
return subtotal - discount_amount
# OR equivalently:
return subtotal * (1 - self.discount_rate)
```

After fixing, run the tests again:
```bash
pytest test_shopping_cart.py -v
```

All tests should now pass!

## Project Structure

```
mcp-debugpy-demo/
├── README.md                    # This file
├── .gitignore                   # Git ignore patterns
├── requirements.txt             # Python dependencies
├── shopping_cart.py             # Main application (with bug)
├── test_shopping_cart.py        # Test suite (exposes the bug)
└── .vscode/
    └── settings.json            # VS Code MCP configuration
```

## Learning Resources

- [MCP Debugpy Documentation](https://github.com/markomanninen/mcp-debugpy)
- [Debug Adapter Protocol (DAP)](https://microsoft.github.io/debug-adapter-protocol/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Python debugpy](https://github.com/microsoft/debugpy)

## Why This Matters

This demo shows how AI agents can help with debugging by:
- **Running tests automatically** to identify failures
- **Setting breakpoints programmatically** at relevant code locations
- **Inspecting variables** to understand program state
- **Stepping through code** to trace execution flow
- **Explaining the bug** in natural language

Traditional debugging requires manual setup, but with MCP tools, an AI agent can orchestrate the entire debugging session!

## Contributing

Found a bug (a real one, not the intentional demo bug!)? Have suggestions? Open an issue or pull request!

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- Built with [mcp-debugpy](https://github.com/markomanninen/mcp-debugpy) by markomanninen
- Uses Microsoft's [debugpy](https://github.com/microsoft/debugpy) debug adapter
- Implements [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) by Anthropic
