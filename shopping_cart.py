"""
A simple shopping cart application with a subtle pricing bug.
"""


class ShoppingCart:
    """Shopping cart that manages items and calculates totals."""

    def __init__(self):
        self.items = []
        self.discount_rate = 0.0

    def add_item(self, name: str, price: float, quantity: int = 1):
        """Add an item to the cart."""
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")

        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def set_discount(self, discount_percent: float):
        """Set a discount percentage (0-100)."""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount_rate = discount_percent / 100

    def calculate_subtotal(self) -> float:
        """Calculate the subtotal before discount."""
        subtotal = 0.0
        for item in self.items:
            subtotal += item["price"] * item["quantity"]
        return subtotal

    def calculate_total(self) -> float:
        """Calculate the final total with discount applied."""
        subtotal = self.calculate_subtotal()
        # BUG: This multiplies by discount rate instead of subtracting it!
        # Should be: subtotal * (1 - self.discount_rate)
        discount_amount = subtotal * self.discount_rate
        return subtotal * discount_amount  # BUG HERE!

    def get_item_count(self) -> int:
        """Get the total number of items in the cart."""
        return sum(item["quantity"] for item in self.items)

    def clear(self):
        """Remove all items from the cart."""
        self.items = []
        self.discount_rate = 0.0


def main():
    """Demo usage of the shopping cart."""
    cart = ShoppingCart()

    # Add some items
    cart.add_item("Laptop", 999.99, 1)
    cart.add_item("Mouse", 29.99, 2)
    cart.add_item("Keyboard", 79.99, 1)

    print(f"Items in cart: {cart.get_item_count()}")
    print(f"Subtotal: ${cart.calculate_subtotal():.2f}")

    # Apply a 10% discount
    cart.set_discount(10)
    total = cart.calculate_total()
    print(f"Total with 10% discount: ${total:.2f}")

    # Expected: $1,079.96 with 10% discount = $971.96
    # Actual: Much smaller due to bug!
    expected = 1079.96 * 0.9
    print(f"Expected total: ${expected:.2f}")

    if abs(total - expected) > 0.01:
        print("WARNING: Total doesn't match expected value!")
    else:
        print("Total is correct.")


if __name__ == "__main__":
    main()
