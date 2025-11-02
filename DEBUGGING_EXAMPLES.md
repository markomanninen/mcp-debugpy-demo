# Debugging Examples with MCP Debugpy

This document provides detailed examples of debugging Python applications using the MCP debugpy tools.

## Example 1: Shopping Cart Discount Bug

See the main [README.md](README.md) for the shopping cart debugging example.

---

## Example 2: Fibonacci Golden Ratio Bug

### The Bug

The `golden_ratio_bug.py` file contains a Fibonacci function with an incorrect base case. The bug causes incorrect golden ratio approximations.

### Buggy Code

```python
def fib(n):
    """Recursive Fibonacci with a bug: wrong base cases."""
    if n <= 0:
        return 0
    if n == 2:
        return 1
    return fib(n-1) + fib(n-2)
```

**Problem**: Missing base case for `n == 1`. When `fib(1)` is called:
- Line 13: `if n <= 0:` is false (1 > 0)
- Line 15: `if n == 2:` is false (1 ≠ 2)
- Line 17: Falls through to `fib(0) + fib(-1)`

This causes the function to recurse into negative values!

### Debugging Session: Tracing fib(5)

Using the MCP debugger, we can trace the complete execution path:

```bash
# Create a test script
cat > test_fib5.py << 'EOF'
from golden_ratio_bug import fib

if __name__ == '__main__':
    result = fib(5)
    print(f"fib(5) = {result}")
EOF

# Debug with breakpoints at lines 13, 15, 17
```

### Complete Execution Trace

When calling `fib(5)`, the debugger encounters these `n` values in order:

| Trace # | n Value | Line | Action |
|---------|---------|------|--------|
| 1 | 5 | 13 | Check if n <= 0 (false) |
| 2 | 5 | 15 | Check if n == 2 (false) |
| 3 | 5 | 17 | Call fib(4) + fib(3) |
| 4 | 4 | 13 | Check if n <= 0 (false) |
| 5 | 4 | 15 | Check if n == 2 (false) |
| 6 | 4 | 17 | Call fib(3) + fib(2) |
| 7 | 3 | 13 | Check if n <= 0 (false) |
| 8 | 3 | 15 | Check if n == 2 (false) |
| 9 | 3 | 17 | Call fib(2) + fib(1) |
| 10 | 2 | 13 | Check if n <= 0 (false) |
| 11 | 2 | 15 | **Check if n == 2 (TRUE)** → returns 1 ✓ |
| 12 | **1** | 13 | Check if n <= 0 (false) |
| 13 | **1** | 15 | Check if n == 2 (false) |
| 14 | **1** | 17 | **Call fib(0) + fib(-1)** ← BUG! |
| 15 | 0 | 13 | Check if n <= 0 (TRUE) → returns 0 ✓ |
| 16 | **-1** | 13 | **Check if n <= 0 (TRUE) → returns 0 ✗ BUG!** |

### Recursive Call Tree

```
fib(5) → 3 (should be 5)
├─ fib(4) → 2 (should be 3)
│  ├─ fib(3) → 1 (should be 2)
│  │  ├─ fib(2) → 1 ✓
│  │  └─ fib(1) → 0 ✗ (should be 1)
│  │     ├─ fib(0) → 0 ✓
│  │     └─ fib(-1) → 0 ✗ (should never be called!)
│  └─ fib(2) → 1 ✓
└─ fib(3) → 1 (should be 2)
   ├─ fib(2) → 1 ✓
   └─ fib(1) → 0 ✗ (should be 1)
      ├─ fib(0) → 0 ✓
      └─ fib(-1) → 0 ✗ (should never be called!)
```

### All n Values Encountered

**Complete sequence**: 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 1, 1, 1, 0, **-1**

**Key Finding**: The last value is **n = -1**, which returns **0** due to the `n <= 0` check.

### Bug Analysis

1. **Root Cause**: Missing base case for `n == 1`
2. **Symptom**: `fib(1)` incorrectly returns 0 instead of 1
3. **Side Effect**: Creates invalid negative recursion `fib(-1)`
4. **Impact**: Entire Fibonacci sequence is shifted, causing wrong results

**Comparison**:
- Correct Fibonacci: `0, 1, 1, 2, 3, 5, 8, 13, 21...`
- Buggy version: `0, 0, 1, 1, 2, 3, 5, 8, 13...` (shifted by one position)

### The Fix

**Option 1** - Add explicit base case for n=1:
```python
def fib(n):
    if n <= 0:
        return 0
    if n == 1:        # ADD THIS
        return 1      # ADD THIS
    if n == 2:
        return 1
    return fib(n-1) + fib(n-2)
```

**Option 2** - Simplify base cases (recommended):
```python
def fib(n):
    if n <= 1:
        return n  # Returns 0 for n=0, 1 for n=1
    return fib(n-1) + fib(n-2)
```

### Verification After Fix

```python
# Correct results:
fib(0) = 0
fib(1) = 1
fib(2) = 1
fib(3) = 2
fib(4) = 3
fib(5) = 5  # ✓ Correct!
```

### MCP Debugger Commands Used

```python
# 1. Launch debugger with breakpoints in the imported module
dap_launch(
    program="test_fib5.py",
    cwd=".",
    breakpoints_by_source={
        "golden_ratio_bug.py": [13, 15, 17]
    },
    wait_for_breakpoint=True
)

# 2. Inspect variables at each breakpoint
dap_locals()

# 3. Continue to next breakpoint
dap_continue()

# 4. Wait for stopped event
dap_wait_for_event("stopped", timeout=5)

# 5. Repeat steps 2-4 to trace through all n values

# 6. Shutdown debugger when done
dap_shutdown()
```

### Key Learning Points

1. **Missing base cases** can cause infinite recursion or invalid negative recursion
2. **Debugger traces** reveal the exact execution path and variable values
3. **Breakpoints on multiple lines** (13, 15, 17) help track control flow
4. **Using `breakpoints_by_source`** allows debugging imported modules
5. **Systematic tracing** from initial call to base cases exposes the bug

---

## Tips for Effective Debugging with MCP

### 1. Strategic Breakpoint Placement

- Place breakpoints at **decision points** (if statements)
- Place breakpoints at **return statements**
- Place breakpoints at **recursive calls**

### 2. Tracing Variable Values

- Check values **before** and **after** critical operations
- Compare **expected vs actual** values
- Track how values **change across recursion levels**

### 3. Understanding Call Stacks

- Use `dap_locals()` to see the **full stack trace**
- Note the **depth of recursion** in stack frames
- Identify **where in the call chain** the bug occurs

### 4. Common Bug Patterns

- **Off-by-one errors**: Missing edge cases (like n=1)
- **Wrong operators**: Multiplying instead of subtracting
- **Incorrect conditions**: Using `==` when you need `<=`
- **Missing validations**: Allowing negative or invalid inputs

### 5. Verification Strategy

- **Test edge cases**: 0, 1, negative numbers
- **Test small values**: Easier to trace and verify
- **Test expected values**: Compare against known correct results
- **Test after fix**: Ensure bug is resolved

---

## Running These Examples

```bash
# 1. Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install pytest
pip install git+https://github.com/markomanninen/mcp-debugpy.git

# 3. Run the buggy programs
python shopping_cart.py
python golden_ratio_bug.py

# 4. See the bugs in action
pytest test_shopping_cart.py -v

# 5. Debug with MCP tools (requires Claude Code, VS Code with MCP, or Claude Desktop)
# Ask your AI: "Debug golden_ratio_bug.py and trace fib(5)"
```

---

## Additional Resources

- [MCP Debugpy Documentation](https://github.com/markomanninen/mcp-debugpy)
- [Debug Adapter Protocol Specification](https://microsoft.github.io/debug-adapter-protocol/)
- [Python debugpy Documentation](https://github.com/microsoft/debugpy)
- [Model Context Protocol](https://modelcontextprotocol.io/)
