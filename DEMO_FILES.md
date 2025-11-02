# Demo Repository File Structure

## Production Files (Ready to Use)

### Core Demo Applications
- **`shopping_cart.py`** - Shopping cart application with a discount calculation bug (line 45)
- **`test_shopping_cart.py`** - Unit tests for the shopping cart
- **`golden_ratio_bug.py`** - Fibonacci function with missing base case bug (demonstrates recursive tracing)
- **`test_fib5.py`** - Test script for debugging fib(5) execution

### Setup & Configuration
- **`configure_mcp.py`** - Script to configure MCP settings for Claude Code/VS Code

### Debug Examples
- **`debug_shopping_cart.py`** - Working example showing how to debug the shopping cart using MCP tools

### Documentation
- **`DEBUGGING_EXAMPLES.md`** - Comprehensive debugging examples with detailed traces

## Directory Structure
```
mcp-debugpy-demo/
├── shopping_cart.py          # Demo app with discount bug
├── test_shopping_cart.py     # Unit tests for shopping cart
├── golden_ratio_bug.py       # Fibonacci with missing base case bug
├── test_fib5.py              # Test script for fib(5) debugging
├── debug_shopping_cart.py    # Debug example
├── configure_mcp.py          # Setup script
├── DEBUGGING_EXAMPLES.md     # Detailed debugging examples and traces
└── .venv/                    # Virtual environment (gitignored)
```

## Usage

1. **Configure MCP Server:**
   ```bash
   python configure_mcp.py
   ```

2. **Run the buggy apps:**
   ```bash
   python shopping_cart.py      # Discount calculation bug
   python golden_ratio_bug.py   # Fibonacci base case bug
   ```

3. **Debug with MCP tools:**
   See `debug_shopping_cart.py` for a working example, or refer to `DEBUGGING_EXAMPLES.md` for detailed debugging traces

4. **Run unit tests:**
   ```bash
   pytest test_shopping_cart.py
   ```

## Clean Repository
All temporary debug/investigation scripts have been removed to keep the repository clean and production-ready.
