# Shopping Cart - Simple

**Prompt:** Write a shopping cart that can add items, remove items, apply discount codes, and calculate totals.

**Output tokens:** 711

## Response

```python
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.discount_codes = {
            "SAVE10": 0.10,
            "SAVE20": 0.20,
            "WELCOME": 0.15
        }
        self.applied_discount = 0.0
    
    def add_item(self, name, price, quantity=1):
        self.items.append({"name": name, "price": price, "quantity": quantity})
    
    def remove_item(self, name):
        self.items = [item for item in self.items if item["name"] != name]
    
    def apply_discount(self, code):
        if code in self.discount_codes:
            self.applied_discount = self.discount_codes[code]
            return True
        return False
    
    def get_subtotal(self):
        return sum(item["price"] * item["quantity"] for item in self.items)
    
    def get_discount_amount(self):
        return self.get_subtotal() * self.applied_discount
    
    def get_total(self):
        return self.get_subtotal() - self.get_discount_amount()
    
    def show_cart(self):
        if not self.items:
            print("Cart is empty")
            return
        
        for item in self.items:
            print(f"{item['name']} x{item['quantity']} - ${item['price']:.2f} each")
        
        print(f"\nSubtotal: ${self.get_subtotal():.2f}")
        if self.applied_discount > 0:
            print(f"Discount: -${self.get_discount_amount():.2f}")
        print(f"Total: ${self.get_total():.2f}")

# Example usage:
cart = ShoppingCart()
cart.add_item("Apple", 1.50, 3)
cart.add_item("Banana", 0.75, 2)
cart.add_item("Orange", 2.00, 1)
cart.show_cart()

print("\nApplying discount code SAVE10...")
cart.apply_discount("SAVE10")
cart.show_cart()

print("\nRemoving Banana...")
cart.remove_item("Banana")
cart.show_cart()
```

This shopping cart does exactly what you asked for in the simplest way possible:

- **Add items**: `add_item(name, price, quantity)`
- **Remove items**: `remove_item(name)` 
- **Apply discounts**: `apply_discount(code)` with predefined codes
- **Calculate totals**: `get_total()`, `get_subtotal()`, `get_discount_amount()`

No unnecessary abstractions, no multiple files, no complex inheritance. Just a single class that stores items in a list and calculates totals with basic math.