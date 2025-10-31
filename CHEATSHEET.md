# MCP Debugpy Demo - Cheat Sheet

Quick reference for using this demo repository.

## Quick Setup (30 seconds)

```bash
git clone https://github.com/markomanninen/mcp-debugpy-demo.git
cd mcp-debugpy-demo
./setup.sh
```

## Quick Test (30 seconds)

```bash
source .venv/bin/activate

# See the bug
python shopping_cart.py

# Run failing tests
pytest test_shopping_cart.py -v
```

## The Bug (Spoiler!)

**Location**: Line 45 of shopping_cart.py

**Wrong**:
```python
return subtotal * discount_amount
```

**Right**:
```python
return subtotal - discount_amount
```

## AI Debugging Commands

### VS Code

Ask in AI chat:
```
"Debug shopping_cart.py using breakpoints at calculate_total"
```

### Claude Desktop

Ask Claude:
```
"Help me debug the shopping cart discount bug using breakpoints"
```

## MCP Tools the AI Will Use

1. `run_tests_json` - Run tests and see failures
2. `dap_launch` - Start debugger with breakpoints
3. `dap_locals` - Inspect variables at breakpoint
4. `dap_step_over` - Step through code line by line
5. `dap_continue` - Continue execution
6. `dap_shutdown` - Stop debugger

## Manual Debugging (Traditional Way)

### Using Python debugger
```bash
python -m pdb shopping_cart.py
(Pdb) b 45
(Pdb) c
(Pdb) p subtotal
(Pdb) p discount_amount
(Pdb) p self.discount_rate
```

### Using pytest debugger
```bash
pytest test_shopping_cart.py::test_calculate_total_with_discount --pdb
```

## File Reference

| File | Purpose | Lines |
|------|---------|-------|
| shopping_cart.py | Main app (buggy) | 93 |
| test_shopping_cart.py | Test suite | 108 |
| README.md | Full documentation | 220 |
| QUICKSTART.md | Fast guide | 173 |
| setup.sh | Installation | 30 |

## Test Results

### Before Fix
- ✓ 7 passing
- ✗ 3 failing (discount-related)

### After Fix (Line 45)
- ✓ 10 passing
- ✗ 0 failing

## Key Locations

- Bug: `shopping_cart.py:45`
- Main test: `test_shopping_cart.py:57`
- Complex test: `test_shopping_cart.py:91`
- Demo function: `shopping_cart.py:58`

## MCP Configuration Files

### VS Code
`.vscode/settings.json`

### Claude Desktop (macOS)
`~/Library/Application Support/Claude/claude_desktop_config.json`

### Claude Desktop (Windows)
`%APPDATA%\Claude\claude_desktop_config.json`

## Environment

### Activate
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Deactivate
```bash
deactivate
```

## Common Issues

### "mcp_server module not found"
```bash
pip install git+https://github.com/markomanninen/mcp-debugpy.git
```

### "pytest not found"
```bash
pip install pytest pytest-asyncio
```

### "Permission denied: setup.sh"
```bash
chmod +x setup.sh
```

## Quick Fix Verification

```bash
# Apply fix to line 45
sed -i '' 's/return subtotal \* discount_amount/return subtotal - discount_amount/' shopping_cart.py

# Run tests
pytest test_shopping_cart.py -v

# Run app
python shopping_cart.py
```

## Documentation

- **Quick Start**: QUICKSTART.md
- **Full Guide**: README.md
- **Technical**: IMPLEMENTATION_NOTES.md
- **This File**: CHEATSHEET.md

## Links

- [mcp-debugpy](https://github.com/markomanninen/mcp-debugpy) - Main library
- [Debug Adapter Protocol](https://microsoft.github.io/debug-adapter-protocol/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## License

MIT License - See LICENSE file

---

**Need help?** See README.md for detailed instructions.

**Found a real bug?** Open an issue on GitHub.

**Want to contribute?** Pull requests welcome!
