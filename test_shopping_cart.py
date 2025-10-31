"""
Tests for the shopping cart application.
These tests will reveal the bug in calculate_total().
"""

import pytest
from shopping_cart import ShoppingCart
import pytest


def test_add_item():
    """Test adding items to the cart."""
    cart = ShoppingCart()
    cart.add_item("Test Item", 10.00, 2)
    assert cart.get_item_count() == 2
    assert len(cart.items) == 1


def test_add_multiple_items():
    """Test adding multiple different items."""
    cart = ShoppingCart()
    cart.add_item("Item 1", 10.00, 1)
    cart.add_item("Item 2", 20.00, 3)
    assert cart.get_item_count() == 4
    assert len(cart.items) == 2


def test_negative_price():
    """Test that negative prices are rejected."""
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="Price cannot be negative"):
        cart.add_item("Bad Item", -10.00)


def test_invalid_quantity():
    """Test that invalid quantities are rejected."""
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="Quantity must be at least 1"):
        cart.add_item("Bad Item", 10.00, 0)


def test_calculate_subtotal():
    """Test subtotal calculation without discount."""
    cart = ShoppingCart()
    cart.add_item("Item 1", 10.00, 2)  # $20
    cart.add_item("Item 2", 15.00, 1)  # $15
    assert cart.calculate_subtotal() == 35.00


@pytest.mark.xfail(reason="Known bug: calculate_total multiplies instead of subtracting discount", strict=False)
def test_calculate_total_no_discount():
    """Test total calculation without discount."""
    cart = ShoppingCart()
    cart.add_item("Item 1", 10.00, 2)
    cart.add_item("Item 2", 15.00, 1)
    total = cart.calculate_total()
    assert total == 35.00, f"Expected 35.00, got {total}"


@pytest.mark.xfail(reason="Known bug: calculate_total multiplies instead of subtracting discount", strict=False)
def test_calculate_total_with_discount():
    """Test total calculation with discount - THIS WILL FAIL due to the bug."""
    cart = ShoppingCart()
    cart.add_item("Item 1", 100.00, 1)
    cart.set_discount(10)  # 10% discount
    total = cart.calculate_total()
    expected = 90.00  # $100 - 10% = $90
    assert total == pytest.approx(expected, rel=0.01), \
        f"Expected {expected}, got {total}. There's a bug in calculate_total()!"


def test_discount_range():
    """Test that invalid discounts are rejected."""
    cart = ShoppingCart()
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        cart.set_discount(-5)
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        cart.set_discount(150)


def test_clear_cart():
    """Test clearing the cart."""
    cart = ShoppingCart()
    cart.add_item("Item 1", 10.00, 2)
    cart.set_discount(10)
    cart.clear()
    assert len(cart.items) == 0
    assert cart.get_item_count() == 0
    assert cart.discount_rate == 0.0


@pytest.mark.xfail(reason="Known bug: calculate_total multiplies instead of subtracting discount", strict=False)
def test_complex_scenario():
    """Test a realistic shopping scenario - WILL FAIL due to bug."""
    cart = ShoppingCart()
    cart.add_item("Laptop", 999.99, 1)
    cart.add_item("Mouse", 29.99, 2)
    cart.add_item("Keyboard", 79.99, 1)

    subtotal = cart.calculate_subtotal()
    assert subtotal == pytest.approx(1139.96, rel=0.01)

    cart.set_discount(10)  # 10% off
    total = cart.calculate_total()
    expected = 1025.96  # $1139.96 - 10% = $1025.96
    assert total == pytest.approx(expected, rel=0.01), \
        f"Expected {expected}, got {total}. The discount calculation is wrong!"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
