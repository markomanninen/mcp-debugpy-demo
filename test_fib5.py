"""Test script to trace fib(5) execution."""
from golden_ratio_bug import fib

if __name__ == '__main__':
    result = fib(5)
    print(f"fib(5) = {result}")
