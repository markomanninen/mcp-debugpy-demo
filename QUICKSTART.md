# Quick Start Guide

Get started with debugging using mcp-debugpy in just a few minutes!

## 1. Setup (2 minutes)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mcp-debugpy-demo.git
cd mcp-debugpy-demo

# Run the automated setup
./setup.sh
```

Or manually:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install pytest
pip install git+https://github.com/markomanninen/mcp-debugpy.git
```

## 2. See the Bug (30 seconds)

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run the application
python shopping_cart.py
```

You'll see:
```
Total with 10% discount: $129950.88
Expected total: $971.96
WARNING: Total doesn't match expected value!
```

That's way off! Let's debug it.

## 3. Run Tests (30 seconds)

```bash
pytest test_shopping_cart.py -v
```

You'll see 3 failing tests:
- `test_calculate_total_no_discount` - Even without discount, total is wrong!
- `test_calculate_total_with_discount` - Gets $1000 instead of $90
- `test_complex_scenario` - Way off the mark

## 4. Debug with AI (Recommended)

### Option A: VS Code

1. Open this repository in VS Code
2. Make sure you have:
   - Python extension installed
   - MCP extension installed
3. Open AI chat panel
4. Ask: **"Debug shopping_cart.py using breakpoints at calculate_total"**

The AI will:
- Set breakpoint at line 45 (the buggy line)
- Launch debugger
- Inspect variables
- Find the bug!

### Option B: Claude Desktop

1. Configure in `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "agentDebug": {
         "command": "/absolute/path/to/.venv/bin/python",
         "args": ["-m", "mcp_server"],
         "cwd": "/absolute/path/to/mcp-debugpy-demo"
       }
     }
   }
   ```

2. Restart Claude Desktop
3. Ask: **"Help debug the shopping cart discount bug"**

## 5. The Bug (Spoiler Alert!)

If you want to find it yourself, stop reading here! Otherwise...

The bug is on **line 45** of [shopping_cart.py](shopping_cart.py:45):

```python
# WRONG:
return subtotal * discount_amount

# SHOULD BE:
return subtotal - discount_amount
# OR:
return subtotal * (1 - self.discount_rate)
```

The code **multiplies** the subtotal by the discount amount instead of **subtracting** it!

Example with 10% discount on $100:
- Discount amount = $100 × 0.10 = $10
- Wrong calculation: $100 × $10 = **$1,000** (way too much!)
- Right calculation: $100 - $10 = **$90** (correct!)

## 6. Fix It

Edit [shopping_cart.py](shopping_cart.py) line 45:

```python
def calculate_total(self) -> float:
    """Calculate the final total with discount applied."""
    subtotal = self.calculate_subtotal()
    discount_amount = subtotal * self.discount_rate
    return subtotal - discount_amount  # FIX: subtract instead of multiply!
```

Verify the fix:

```bash
pytest test_shopping_cart.py -v
python shopping_cart.py
```

All tests should pass!

## What Just Happened?

You used an AI agent with MCP debugpy tools to:

1. **Run tests** (`run_tests_json`) to identify failing tests
2. **Launch debugger** (`dap_launch`) with breakpoints
3. **Inspect variables** (`dap_locals`) to see actual values
4. **Step through code** (`dap_step_over`) to trace execution
5. **Find the root cause** by analyzing the buggy logic

All through natural language conversation with an AI agent!

## Next Steps

- Try debugging more complex scenarios
- Set conditional breakpoints
- Inspect nested data structures
- Debug async code

Check out the main [README.md](README.md) for more details and advanced usage!
