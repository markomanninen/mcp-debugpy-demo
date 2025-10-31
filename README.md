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

### Option A: VS Code with MCP Extension

The repository includes [.vscode/settings.json](.vscode/settings.json) pre-configured for mcp-debugpy.

1. Open this repository in VS Code
2. Open the AI chat panel (make sure MCP extension is installed)
3. Ask the AI: "Debug the shopping_cart.py bug using breakpoints"

The AI agent can use these MCP tools:
- `dap_launch` - Start debugging with breakpoints
- `dap_locals` - Inspect variable values
- `dap_step_over` / `dap_step_in` - Step through code
- `dap_continue` - Continue execution
- `run_tests_json` - Run tests and analyze failures

### Option B: Claude Desktop

1. Configure Claude Desktop with the mcp-debugpy server:

   **macOS/Linux**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`

   **Windows**: Edit `%APPDATA%\Claude\claude_desktop_config.json`

   ```json
   {
     "mcpServers": {
       "agentDebug": {
         "command": "/full/path/to/mcp-debugpy-demo/.venv/bin/python",
         "args": ["-m", "mcp_server"],
         "cwd": "/full/path/to/mcp-debugpy-demo"
       }
     }
   }
   ```

2. Restart Claude Desktop
3. Start a conversation: "Help me debug the bug in shopping_cart.py"

### Example Debugging Session

Ask the AI assistant:

> "There's a bug in shopping_cart.py causing wrong discount calculations. Help me debug it by:
> 1. Running the tests to see what's failing
> 2. Setting a breakpoint in calculate_total()
> 3. Inspecting the variables when the discount is applied
> 4. Finding and explaining the bug"

The AI will:
1. Run `run_tests_json` to see the failing tests
2. Use `dap_launch` to start debugging with a breakpoint at line 45
3. Use `dap_locals` to inspect `subtotal`, `discount_amount`, and `self.discount_rate`
4. Use `dap_step_over` to step through the calculation
5. Identify that line 45 multiplies instead of subtracting the discount

### Manual Debugging (Traditional Way)

If you want to debug manually without MCP:

```bash
# Run with Python debugger
python -m pdb shopping_cart.py

# Set breakpoint
(Pdb) b shopping_cart.py:45

# Run
(Pdb) continue

# Inspect variables
(Pdb) p subtotal
(Pdb) p discount_amount
(Pdb) p self.discount_rate
```

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
