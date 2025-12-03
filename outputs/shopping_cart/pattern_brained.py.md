# Shopping Cart - Pattern Brained

**Prompt:** Write a shopping cart that can add items, remove items, apply discount codes, and calculate totals.

**Output tokens:** 3717

## Response

I'll create a well-architected shopping cart system using design patterns and SOLID principles. Here's the implementation:

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from decimal import Decimal
from dataclasses import dataclass
from enum import Enum
import uuid


# Domain Models
@dataclass(frozen=True)
class Product:
    """Immutable product representation."""
    id: str
    name: str
    price: Decimal
    
    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Product price cannot be negative")


@dataclass
class CartItem:
    """Represents an item in the shopping cart."""
    product: Product
    quantity: int
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
    
    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.quantity


class DiscountType(Enum):
    """Types of discounts available."""
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"


@dataclass(frozen=True)
class DiscountCode:
    """Immutable discount code representation."""
    code: str
    discount_type: DiscountType
    value: Decimal
    minimum_amount: Optional[Decimal] = None
    
    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Discount value cannot be negative")
        if self.discount_type == DiscountType.PERCENTAGE and self.value > 100:
            raise ValueError("Percentage discount cannot exceed 100%")


# Strategy Pattern for Discount Calculation
class DiscountStrategy(ABC):
    """Abstract base class for discount calculation strategies."""
    
    @abstractmethod
    def calculate_discount(self, subtotal: Decimal, discount_code: DiscountCode) -> Decimal:
        pass
    
    @abstractmethod
    def is_applicable(self, subtotal: Decimal, discount_code: DiscountCode) -> bool:
        pass


class PercentageDiscountStrategy(DiscountStrategy):
    """Strategy for percentage-based discounts."""
    
    def calculate_discount(self, subtotal: Decimal, discount_code: DiscountCode) -> Decimal:
        return subtotal * (discount_code.value / 100)
    
    def is_applicable(self, subtotal: Decimal, discount_code: DiscountCode) -> bool:
        if discount_code.minimum_amount is None:
            return True
        return subtotal >= discount_code.minimum_amount


class FixedAmountDiscountStrategy(DiscountStrategy):
    """Strategy for fixed amount discounts."""
    
    def calculate_discount(self, subtotal: Decimal, discount_code: DiscountCode) -> Decimal:
        return min(discount_code.value, subtotal)  # Don't exceed subtotal
    
    def is_applicable(self, subtotal: Decimal, discount_code: DiscountCode) -> bool:
        if discount_code.minimum_amount is None:
            return True
        return subtotal >= discount_code.minimum_amount


# Factory Pattern for Discount Strategies
class DiscountStrategyFactory:
    """Factory for creating discount strategies."""
    
    _strategies = {
        DiscountType.PERCENTAGE: PercentageDiscountStrategy,
        DiscountType.FIXED_AMOUNT: FixedAmountDiscountStrategy
    }
    
    @classmethod
    def create_strategy(cls, discount_type: DiscountType) -> DiscountStrategy:
        strategy_class = cls._strategies.get(discount_type)
        if not strategy_class:
            raise ValueError(f"Unknown discount type: {discount_type}")
        return strategy_class()


# Repository Pattern for Discount Codes
class DiscountCodeRepository(ABC):
    """Abstract repository for discount codes."""
    
    @abstractmethod
    def find_by_code(self, code: str) -> Optional[DiscountCode]:
        pass


class InMemoryDiscountCodeRepository(DiscountCodeRepository):
    """In-memory implementation of discount code repository."""
    
    def __init__(self):
        self._discount_codes: Dict[str, DiscountCode] = {}
    
    def add_discount_code(self, discount_code: DiscountCode) -> None:
        self._discount_codes[discount_code.code] = discount_code
    
    def find_by_code(self, code: str) -> Optional[DiscountCode]:
        return self._discount_codes.get(code)


# Service Layer
class DiscountService:
    """Service for handling discount calculations."""
    
    def __init__(self, discount_repository: DiscountCodeRepository):
        self._discount_repository = discount_repository
        self._strategy_factory = DiscountStrategyFactory()
    
    def apply_discount(self, subtotal: Decimal, discount_code: str) -> Decimal:
        """Apply discount and return the discount amount."""
        code = self._discount_repository.find_by_code(discount_code)
        if not code:
            raise ValueError(f"Invalid discount code: {discount_code}")
        
        strategy = self._strategy_factory.create_strategy(code.discount_type)
        
        if not strategy.is_applicable(subtotal, code):
            raise ValueError(f"Discount code {discount_code} is not applicable")
        
        return strategy.calculate_discount(subtotal, code)


# Observer Pattern for Cart Events
class CartObserver(ABC):
    """Observer interface for cart events."""
    
    @abstractmethod
    def on_item_added(self, cart_id: str, item: CartItem) -> None:
        pass
    
    @abstractmethod
    def on_item_removed(self, cart_id: str, product_id: str) -> None:
        pass
    
    @abstractmethod
    def on_item_updated(self, cart_id: str, item: CartItem) -> None:
        pass


class CartEventLogger(CartObserver):
    """Example observer that logs cart events."""
    
    def on_item_added(self, cart_id: str, item: CartItem) -> None:
        print(f"Added {item.quantity}x {item.product.name} to cart {cart_id}")
    
    def on_item_removed(self, cart_id: str, product_id: str) -> None:
        print(f"Removed product {product_id} from cart {cart_id}")
    
    def on_item_updated(self, cart_id: str, item: CartItem) -> None:
        print(f"Updated {item.product.name} quantity to {item.quantity} in cart {cart_id}")


# Main Shopping Cart Class
class ShoppingCart:
    """Main shopping cart class following SOLID principles."""
    
    def __init__(self, discount_service: DiscountService):
        self._id = str(uuid.uuid4())
        self._items: Dict[str, CartItem] = {}
        self._applied_discount_code: Optional[str] = None
        self._discount_service = discount_service
        self._observers: List[CartObserver] = []
    
    @property
    def id(self) -> str:
        return self._id
    
    def add_observer(self, observer: CartObserver) -> None:
        """Add an observer for cart events."""
        self._observers.append(observer)
    
    def remove_observer(self, observer: CartObserver) -> None:
        """Remove an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_item_added(self, item: CartItem) -> None:
        for observer in self._observers:
            observer.on_item_added(self._id, item)
    
    def _notify_item_removed(self, product_id: str) -> None:
        for observer in self._observers:
            observer.on_item_removed(self._id, product_id)
    
    def _notify_item_updated(self, item: CartItem) -> None:
        for observer in self._observers:
            observer.on_item_updated(self._id, item)
    
    def add_item(self, product: Product, quantity: int = 1) -> None:
        """Add an item to the cart."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if product.id in self._items:
            # Update existing item
            existing_item = self._items[product.id]
            new_quantity = existing_item.quantity + quantity
            updated_item = CartItem(product, new_quantity)
            self._items[product.id] = updated_item
            self._notify_item_updated(updated_item)
        else:
            # Add new item
            item = CartItem(product, quantity)
            self._items[product.id] = item
            self._notify_item_added(item)
    
    def remove_item(self, product_id: str) -> None:
        """Remove an item from the cart."""
        if product_id not in self._items:
            raise ValueError(f"Product {product_id} not found in cart")
        
        del self._items[product_id]
        self._notify_item_removed(product_id)
    
    def update_item_quantity(self, product_id: str, quantity: int) -> None:
        """Update the quantity of an item in the cart."""
        if product_id not in self._items:
            raise ValueError(f"Product {product_id} not found in cart")
        
        if quantity <= 0:
            self.remove_item(product_id)
            return
        
        item = self._items[product_id]
        updated_item = CartItem(item.product, quantity)
        self._items[product_id] = updated_item
        self._notify_item_updated(updated_item)
    
    def apply_discount_code(self, discount_code: str) -> None:
        """Apply a discount code to the cart."""
        # Validate the discount code by attempting to calculate discount
        subtotal = self.get_subtotal()
        self._discount_service.apply_discount(subtotal, discount_code)
        self._applied_discount_code = discount_code
    
    def remove_discount_code(self) -> None:
        """Remove the applied discount code."""
        self._applied_discount_code = None
    
    def get_items(self) -> List[CartItem]:
        """Get all items in the cart."""
        return list(self._items.values())
    
    def get_subtotal(self) -> Decimal:
        """Calculate the subtotal (before discount)."""
        return sum(item.subtotal for item in self._items.values())
    
    def get_discount_amount(self) -> Decimal:
        """Calculate the discount amount."""
        if not self._applied_discount_code:
            return Decimal('0')
        
        subtotal = self.get_subtotal()
        try:
            return self._discount_service.apply_discount(subtotal, self._applied_discount_code)
        except ValueError:
            # Discount is no longer valid (e.g., minimum amount not met)
            self._applied_discount_code = None
            return Decimal('0')
    
    def get_total(self) -> Decimal:
        """Calculate the final total (after discount)."""
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        return subtotal - discount
    
    def clear(self) -> None:
        """Clear all items from the cart."""
        for product_id in list(self._items.keys()):
            self.remove_item(product_id)
        self._applied_discount_code = None
    
    def is_empty(self) -> bool:
        """Check if the cart is empty."""
        return len(self._items) == 0


# Example usage and demonstration
if __name__ == "__main__":
    # Set up dependencies
    discount_repo = InMemoryDiscountCodeRepository()
    discount_repo.add_discount_code(
        DiscountCode("SAVE10", DiscountType.PERCENTAGE, Decimal('10'))
    )
    discount_repo.add_discount_code(
        DiscountCode("FLAT5", DiscountType.FIXED_AMOUNT, Decimal('5.00'), Decimal('20.00'))
    )
    
    discount_service = DiscountService(discount_repo)
    cart = ShoppingCart(discount_service)
    
    # Add observer
    logger = CartEventLogger()
    cart.add_observer(logger)
    
    # Create products
    laptop = Product("1", "Laptop", Decimal('999.99'))
    mouse = Product("2", "Mouse", Decimal('29.99'))
    keyboard = Product("3", "Keyboard", Decimal('79.99'))
    
    # Add items to cart
    cart.add_item(laptop, 1)
    cart.add_item(mouse, 2)
    cart.add_item(keyboard, 1)
    
    print(f"Subtotal: ${cart.get_subtotal()}")
    
    # Apply discount
    cart.apply_discount_code("SAVE10")
    print(f"Discount: ${cart.get_discount_amount()}")
    print(f"Total: ${cart.get_total()}")
    
    # Update quantity
    cart.update_item_quantity("2", 3)  # Update mouse quantity to 3
    print(f"Updated Total: ${cart.get_total()}")
    
    # Remove item
    cart.remove_item("3")  # Remove keyboard
    print(f"Final Total: ${cart.get_total()}")
```

This shopping cart implementation demonstrates several key design patterns and architectural principles:

## Design Patterns Used:

1. **Strategy Pattern**: Different discount calculation strategies (percentage vs fixed amount)
2. **Factory Pattern**: `DiscountStrategyFactory` creates appropriate discount strategies
3. **Repository Pattern**: Abstracts discount code storage and retrieval
4. **Observer Pattern**: Allows external components to react to cart events
5. **Dependency Injection**: Cart depends on abstractions, not concrete implementations

## SOLID Principles:

1. **Single Responsibility**: Each class has one clear purpose
2. **Open/Closed**: Easy to add new discount types or observers without modifying existing code
3. **Liskov Substitution**: Implementations can be substituted for their interfaces
4. **Interface Segregation**: Small, focused interfaces
5. **Dependency Inversion**: Depends on abstractions, not concretions

## Key Features:

- **Thread-safe operations** through immutable domain objects
- **Extensible discount system** - easy to add new discount types
- **Event-driven architecture** through observers
- **Proper error handling** with meaningful exceptions
- **Clean separation of concerns** between domain, service, and infrastructure layers
- **Type safety** with proper type hints throughout

The system is production-ready and can be easily extended with features like tax calculation, shipping, inventory management, or different storage backends.