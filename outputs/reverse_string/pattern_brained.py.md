# Reverse String - Pattern Brained

**Prompt:** Write a function that reverses a string.

**Output tokens:** 2023

## Response

I'll create a well-architected string reversal solution using proper design patterns and SOLID principles.

```python
from abc import ABC, abstractmethod
from typing import Optional, Protocol
from enum import Enum


class ReversalStrategy(Protocol):
    """Protocol defining the interface for string reversal strategies."""
    
    def reverse(self, text: str) -> str:
        """Reverse the given text string."""
        ...


class ReversalMethod(Enum):
    """Enumeration of available reversal methods."""
    SLICE = "slice"
    ITERATIVE = "iterative" 
    RECURSIVE = "recursive"


class SliceReversalStrategy:
    """Strategy implementing string reversal using Python slicing."""
    
    def reverse(self, text: str) -> str:
        """Reverse string using slice notation [::-1]."""
        return text[::-1]


class IterativeReversalStrategy:
    """Strategy implementing string reversal using iterative approach."""
    
    def reverse(self, text: str) -> str:
        """Reverse string by iterating through characters."""
        return ''.join(reversed(text))


class RecursiveReversalStrategy:
    """Strategy implementing string reversal using recursion."""
    
    def reverse(self, text: str) -> str:
        """Reverse string using recursive divide-and-conquer."""
        if len(text) <= 1:
            return text
        return text[-1] + self.reverse(text[:-1])


class ReversalStrategyFactory:
    """Factory for creating reversal strategy instances."""
    
    _strategies = {
        ReversalMethod.SLICE: SliceReversalStrategy,
        ReversalMethod.ITERATIVE: IterativeReversalStrategy,
        ReversalMethod.RECURSIVE: RecursiveReversalStrategy,
    }
    
    @classmethod
    def create_strategy(self, method: ReversalMethod) -> ReversalStrategy:
        """Create and return a reversal strategy instance."""
        if method not in self._strategies:
            raise ValueError(f"Unsupported reversal method: {method}")
        
        return self._strategies[method]()
    
    @classmethod
    def get_available_methods(self) -> list[ReversalMethod]:
        """Return list of available reversal methods."""
        return list(self._strategies.keys())


class StringValidator:
    """Utility class for validating string inputs."""
    
    @staticmethod
    def validate_input(text: Optional[str]) -> str:
        """Validate and normalize input string."""
        if text is None:
            raise ValueError("Input text cannot be None")
        
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        
        return text


class StringReverser:
    """Main service class for string reversal operations."""
    
    def __init__(self, strategy: Optional[ReversalStrategy] = None):
        """Initialize with optional custom strategy."""
        self._strategy = strategy or SliceReversalStrategy()
        self._validator = StringValidator()
    
    def set_strategy(self, strategy: ReversalStrategy) -> None:
        """Change the reversal strategy at runtime."""
        self._strategy = strategy
    
    def reverse(self, text: str) -> str:
        """
        Reverse the given string using the current strategy.
        
        Args:
            text: The string to reverse
            
        Returns:
            The reversed string
            
        Raises:
            ValueError: If text is None
            TypeError: If text is not a string
        """
        validated_text = self._validator.validate_input(text)
        return self._strategy.reverse(validated_text)


class StringReversalService:
    """
    High-level service providing string reversal functionality.
    
    This class serves as a facade, simplifying the interface for clients
    while encapsulating the complexity of strategy selection and validation.
    """
    
    def __init__(self):
        """Initialize the service with default strategy."""
        self._reverser = StringReverser()
        self._factory = ReversalStrategyFactory()
    
    def reverse_string(
        self, 
        text: str, 
        method: ReversalMethod = ReversalMethod.SLICE
    ) -> str:
        """
        Reverse a string using the specified method.
        
        Args:
            text: The string to reverse
            method: The reversal method to use
            
        Returns:
            The reversed string
        """
        strategy = self._factory.create_strategy(method)
        self._reverser.set_strategy(strategy)
        return self._reverser.reverse(text)
    
    def get_available_methods(self) -> list[ReversalMethod]:
        """Get list of available reversal methods."""
        return self._factory.get_available_methods()


# Convenience function for simple usage
def reverse_string(text: str, method: ReversalMethod = ReversalMethod.SLICE) -> str:
    """
    Convenience function to reverse a string.
    
    Args:
        text: The string to reverse
        method: The reversal method to use (default: slice)
        
    Returns:
        The reversed string
        
    Example:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("world", ReversalMethod.RECURSIVE)
        'dlrow'
    """
    service = StringReversalService()
    return service.reverse_string(text, method)


# Example usage and testing
if __name__ == "__main__":
    # Demonstrate different usage patterns
    
    # Simple function usage
    print("Simple function usage:")
    print(f"reverse_string('Hello World'): {reverse_string('Hello World')}")
    
    # Service usage with different strategies
    print("\nService usage with different strategies:")
    service = StringReversalService()
    
    text = "Design Patterns"
    for method in service.get_available_methods():
        result = service.reverse_string(text, method)
        print(f"{method.value}: '{text}' -> '{result}'")
    
    # Direct class usage for more control
    print("\nDirect class usage:")
    reverser = StringReverser()
    
    # Change strategies at runtime
    strategies = [
        ("Slice", SliceReversalStrategy()),
        ("Iterative", IterativeReversalStrategy()),
        ("Recursive", RecursiveReversalStrategy()),
    ]
    
    test_text = "Architecture"
    for name, strategy in strategies:
        reverser.set_strategy(strategy)
        result = reverser.reverse(test_text)
        print(f"{name} strategy: '{test_text}' -> '{result}'")
    
    # Error handling demonstration
    print("\nError handling:")
    try:
        reverse_string(None)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    try:
        reverse_string(123)
    except TypeError as e:
        print(f"Caught expected error: {e}")
```

This implementation demonstrates several key design patterns and architectural principles:

## Design Patterns Used:

1. **Strategy Pattern**: Multiple algorithms for string reversal that can be switched at runtime
2. **Factory Pattern**: `ReversalStrategyFactory` creates strategy instances
3. **Facade Pattern**: `StringReversalService` provides a simplified interface
4. **Protocol/Interface Segregation**: `ReversalStrategy` protocol defines the contract

## SOLID Principles:

1. **Single Responsibility**: Each class has one clear purpose
2. **Open/Closed**: Easy to add new reversal strategies without modifying existing code
3. **Liskov Substitution**: All strategies are interchangeable
4. **Interface Segregation**: Clean, focused protocols
5. **Dependency Inversion**: High-level modules depend on abstractions

## Key Features:

- **Extensible**: Easy to add new reversal algorithms
- **Configurable**: Multiple ways to use the functionality
- **Robust**: Comprehensive input validation and error handling
- **Testable**: Clear separation of concerns makes unit testing straightforward
- **Production-ready**: Proper typing, documentation, and error handling

The solution provides both simple function usage and full object-oriented architecture, allowing clients to choose the appropriate level of complexity for their needs.