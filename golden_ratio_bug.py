"""
Buggy golden ratio approximation using recursive Fibonacci.
Run this script to print approximations of the golden ratio phi for increasing n.
This intentionally contains a bug in the Fibonacci base case to practice debugging.
"""

import sys


def fib(n):
    """Recursive Fibonacci with a bug: wrong base cases."""
    # Intentional bug: base case only handles n <= 0 instead of n <= 1
    if n <= 0:
        return 0
    if n == 2:
        return 1
    return fib(n-1) + fib(n-2)


def approx_phi(n):
    """Return approximation of phi using F(n)/F(n-1). n should be >= 2."""
    if n < 2:
        raise ValueError("n must be >= 2")
    return fib(n) / fib(n-1)


def main():
    max_n = 10
    if len(sys.argv) > 1:
        try:
            max_n = int(sys.argv[1])
        except ValueError:
            print("Invalid integer, using default 10")
    for i in range(2, max_n+1):
        print(f"n={i}: phi≈{approx_phi(i)}")


if __name__ == '__main__':
    main()
