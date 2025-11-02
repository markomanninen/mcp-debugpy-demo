#!/usr/bin/env python3
"""
Debug the shopping cart bug by stepping through calculate_total() method.
"""
import asyncio
import json
import sys
from pathlib import Path

# Add mcp-debugpy src to path
mcp_debugpy_path = Path(__file__).parent.parent / "mcp-debugpy" / "src"
sys.path.insert(0, str(mcp_debugpy_path))

# Import the MCP server module
import mcp_server


async def main():
    """Debug shopping_cart.py calculate_total method"""

    program_path = Path(__file__).parent / "shopping_cart.py"

    config = {
        "program": str(program_path.absolute()),
        "cwd": str(program_path.parent.absolute()),
        "breakpoints": [44, 45],  # Lines inside calculate_total where the bug is
        "stop_on_entry": False,
        "wait_for_breakpoint": True,
        "breakpoint_timeout": 30
    }

    print("=" * 70)
    print("DEBUGGING SHOPPING CART BUG")
    print("=" * 70)
    print(f"\nProgram: {program_path.name}")
    print(f"Breakpoints: Lines {config['breakpoints']} (inside calculate_total method)")
    print()

    try:
        # Launch debug session
        print("Launching debug session...")
        result = await mcp_server.dap_launch(
            program=config["program"],
            breakpoints=config["breakpoints"],
            cwd=config["cwd"],
            stop_on_entry=config["stop_on_entry"],
            wait_for_breakpoint=config["wait_for_breakpoint"],
            breakpoint_timeout=config["breakpoint_timeout"]
        )

        # Check if we hit the breakpoint
        if not result.get("stoppedEvent"):
            print("[ERROR] Did not hit breakpoint!")
            return 1

        stopped = result["stoppedEvent"]
        reason = stopped.get("body", {}).get("reason", "unknown")
        print(f"\n[SUCCESS] Program stopped at breakpoint: {reason}")

        # Get locals at the breakpoint
        print("\nInspecting variables at breakpoint...")
        locals_result = await mcp_server.dap_locals()

        print("\n" + "=" * 70)
        print("STACK TRACE")
        print("=" * 70)
        if locals_result.get("stackFrames"):
            for i, frame in enumerate(locals_result["stackFrames"]):
                name = frame.get("name", "unknown")
                line = frame.get("line", "?")
                source = frame.get("source", {}).get("path", "")
                print(f"  Frame #{i}: {name} at line {line}")
                print(f"            {Path(source).name if source else ''}")

        print("\n" + "=" * 70)
        print("LOCAL VARIABLES")
        print("=" * 70)
        print(json.dumps(locals_result, indent=2, default=str))

        # Try to extract variables properly
        if "scopes" in locals_result:
            for scope in locals_result["scopes"]:
                if "variables" in scope:
                    print(f"\nScope: {scope.get('name', 'unknown')}")
                    for var in scope["variables"]:
                        if isinstance(var, dict):
                            name = var.get("name", "unknown")
                            value = var.get("value", "N/A")
                            var_type = var.get("type", "")
                            print(f"  {name} = {value}  ({var_type})")

        # Step over to see the calculation
        print("\n" + "=" * 70)
        print("STEPPING OVER TO EXECUTE LINE 45 (THE BUG)")
        print("=" * 70)
        await mcp_server.dap_step_over()

        # Wait for stopped event after step
        await mcp_server.dap_wait_for_event("stopped", timeout=5)

        # Get locals again to see the result
        print("\nInspecting variables after executing line 45...")
        locals_after = await mcp_server.dap_locals()

        print("\n" + "=" * 70)
        print("LOCAL VARIABLES AFTER BUG LINE")
        print("=" * 70)

        # Try to extract variables properly
        if "scopes" in locals_after:
            for scope in locals_after["scopes"]:
                if "variables" in scope:
                    print(f"\nScope: {scope.get('name', 'unknown')}")
                    for var in scope["variables"]:
                        if isinstance(var, dict):
                            name = var.get("name", "unknown")
                            value = var.get("value", "N/A")
                            var_type = var.get("type", "")
                            print(f"  {name} = {value}  ({var_type})")

        print("\n" + "=" * 70)
        print("BUG ANALYSIS")
        print("=" * 70)
        print("\nThe bug is on line 45:")
        print("  return subtotal * discount_amount")
        print("\nThis MULTIPLIES subtotal by discount_amount instead of SUBTRACTING!")
        print("\nCorrect formula should be:")
        print("  return subtotal - discount_amount")
        print("  OR: return subtotal * (1 - self.discount_rate)")
        print("\nExample with 10% discount on $1139.96:")
        print(f"  subtotal = $1139.96")
        print(f"  discount_rate = 0.10")
        print(f"  discount_amount = $1139.96 * 0.10 = $113.996")
        print(f"  WRONG: $1139.96 * $113.996 = $129,993.60 (absurdly high!)")
        print(f"  CORRECT: $1139.96 - $113.996 = $1,025.96")

        # Continue to let program finish
        print("\nContinuing execution...")
        await mcp_server.dap_continue()

        # Cleanup
        if mcp_server._dap_client:
            await asyncio.sleep(1)  # Give it time to finish
            await mcp_server._dap_client.close()
            mcp_server._dap_client = None

        print("\n[SUCCESS] Debug session complete")
        return 0

    except Exception as e:
        print(f"\n[ERROR] Debug session failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
