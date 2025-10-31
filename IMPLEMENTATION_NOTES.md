# Implementation Notes

This document explains the demo repository design and implementation decisions.

## Repository Structure

```
mcp-debugpy-demo/
├── shopping_cart.py         # Main application with bug
├── test_shopping_cart.py     # Test suite (10 tests, 3 fail)
├── setup.sh                  # Automated setup script
├── requirements.txt          # Dependencies
├── README.md                 # Comprehensive documentation
├── QUICKSTART.md            # Fast-track guide
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore patterns
└── .vscode/
    └── settings.json        # MCP configuration for VS Code
```

## The Bug

**Location**: [shopping_cart.py:45](shopping_cart.py#L45)

**Type**: Logic error in discount calculation

**What's wrong**:
```python
# Current (WRONG):
return subtotal * discount_amount

# Should be:
return subtotal - discount_amount
```

**Why it's wrong**:
- When discount_rate is 0.1 (10%), discount_amount = subtotal * 0.1
- Current code: total = subtotal * (subtotal * 0.1) = subtotal²  * 0.1
- This causes exponential growth instead of subtraction
- Example: $100 with 10% discount gives $1,000 instead of $90

**When it manifests**:
- Only when discount is applied (discount_rate > 0)
- Test without discount passes (returns 0.0 which happens to match when discount_rate=0)
- Tests with discount spectacularly fail

## Test Coverage

The test suite has **10 tests** covering:

### Passing Tests (7)
1. `test_add_item` - Basic item addition
2. `test_add_multiple_items` - Multiple items
3. `test_negative_price` - Input validation
4. `test_invalid_quantity` - Input validation
5. `test_calculate_subtotal` - Subtotal calculation
6. `test_discount_range` - Discount validation
7. `test_clear_cart` - Cart clearing

### Failing Tests (3) - Due to the Bug
1. `test_calculate_total_no_discount` - Expects 35.00, gets 0.0
2. `test_calculate_total_with_discount` - Expects 90.00, gets 1000.0
3. `test_complex_scenario` - Expects 1025.96, gets 129950.88

## Design Decisions

### Why This Bug?

1. **Subtle but obvious** - Easy to spot when you look at the code, but easy to miss without debugging
2. **Clear symptoms** - Tests fail with obvious wrong values
3. **Demonstrates variable inspection** - Need to inspect `subtotal`, `discount_amount`, and `discount_rate` to understand
4. **Realistic** - Similar to real bugs (wrong operator, copy-paste error)

### Why Shopping Cart?

1. **Familiar domain** - Everyone understands shopping and discounts
2. **Testable** - Easy to write assertions with expected values
3. **Visual impact** - Seeing $129,950 instead of $1,025 is striking
4. **Multiple operations** - Shows item addition, subtotal calculation, and discount application

### File Organization

- **Single application file** - Easy to navigate and debug
- **Single test file** - All tests in one place
- **Automated setup** - `setup.sh` handles all installation
- **VS Code integration** - Pre-configured for immediate use
- **Clear documentation** - README for depth, QUICKSTART for speed

## Debugging Strategy

When debugging with mcp-debugpy, the AI agent should:

1. **Run tests first** - Use `run_tests_json` to see failures
2. **Identify the bug location** - analyze test failures pointing to `calculate_total()`
3. **Set breakpoint** - Use `dap_launch` with breakpoint at line 45
4. **Inspect variables** - Use `dap_locals` to see:
   - `subtotal` (correct value)
   - `discount_amount` (correct value)
   - Result of multiplication (wrong!)
5. **Step through** - Use `dap_step_over` to trace execution
6. **Identify the issue** - Multiplying instead of subtracting

## MCP Configuration

The `.vscode/settings.json` configures the MCP server:

```json
{
  "mcp.servers.agentDebug": {
    "command": "${workspaceFolder}/.venv/bin/python",
    "args": ["-m", "mcp_server"],
    "cwd": "${workspaceFolder}"
  }
}
```

**Key points**:
- Uses workspace-relative paths
- Runs `mcp_server` as a module (requires proper installation)
- Working directory is the project root

## Installation Flow

### Via setup.sh
1. Creates virtual environment
2. Activates it
3. Installs pytest
4. Installs mcp-debugpy from GitHub

### Manual
1. User creates venv
2. User activates
3. User installs dependencies
4. User installs mcp-debugpy

Both flows work with the git URL until mcp-debugpy is published to PyPI.

## Future Enhancements

Potential additions for future versions:

1. **More complex bugs** - Async bugs, race conditions, edge cases
2. **Multiple files** - Bugs spanning multiple modules
3. **Configuration files** - Bugs in config parsing
4. **API integration** - Bugs in HTTP request handling
5. **Database interactions** - SQL query bugs
6. **Performance issues** - Memory leaks, slow algorithms

## Testing the Demo

To verify everything works:

```bash
cd /tmp/mcp-debugpy-demo

# Test the bug manifests
python shopping_cart.py  # Should show warning

# Test suite fails correctly
pytest test_shopping_cart.py -v  # 3 failures expected

# Apply the fix (edit line 45):
# Change: return subtotal * discount_amount
# To:     return subtotal - discount_amount

# Verify the fix
pytest test_shopping_cart.py -v  # All pass
python shopping_cart.py  # No warning
```

## GitHub Repository Checklist

Before pushing to GitHub:

- [x] LICENSE file (MIT)
- [x] README.md with comprehensive docs
- [x] QUICKSTART.md for fast onboarding
- [x] .gitignore for Python projects
- [x] requirements.txt
- [x] setup.sh with proper permissions
- [x] .vscode/settings.json for MCP
- [x] Application code with documented bug
- [x] Test suite with clear failures
- [ ] GitHub repository created
- [ ] Initial commit pushed
- [ ] Repository description set
- [ ] Topics added (mcp, debugpy, python, debugging, ai, demo)
- [ ] README preview looks good
- [ ] Social media preview image (optional)

## License

MIT License - See [LICENSE](LICENSE) file for details.
