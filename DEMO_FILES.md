# Demo Repository File Structure

## Production Files (Ready to Use)

### Core Demo Application
- **`shopping_cart.py`** - Shopping cart application with a discount calculation bug (line 45)
- **`test_shopping_cart.py`** - Unit tests for the shopping cart

### Setup & Configuration
- **`configure_mcp.py`** - Script to configure MCP settings for Claude Code/VS Code

### Debug Examples
- **`debug_shopping_cart.py`** - Working example showing how to debug the shopping cart using MCP tools

## Directory Structure
```
mcp-debugpy-demo/
├── shopping_cart.py          # Demo app with bug
├── test_shopping_cart.py     # Unit tests
├── debug_shopping_cart.py    # Debug example
├── configure_mcp.py          # Setup script

└── .venv/                    # Virtual environment (gitignored)
```

## Usage

1. **Configure MCP Server:**
   ```bash
   python configure_mcp.py
   ```

2. **Run the buggy app:**
   ```bash
   python shopping_cart.py
   ```
   Expected bug: Discount multiplies instead of subtracts

3. **Debug with MCP tools:**
   See `debug_shopping_cart.py` for a working example

4. **Run unit tests:**
   ```bash
   pytest test_shopping_cart.py
   ```

## Clean Repository
All temporary debug/investigation scripts have been removed to keep the repository clean and production-ready.
