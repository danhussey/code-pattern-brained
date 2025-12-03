# Palindrome Checker - Pattern Brained

**Prompt:** Write a function that checks if a string is a palindrome.

**Output tokens:** 2458

## Response

I'll create a well-architected palindrome checker using proper design patterns and SOLID principles.

```python
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
from enum import Enum
import re


class PalindromeStrategy(ABC):
    """Strategy interface for different palindrome checking algorithms."""
    
    @abstractmethod
    def is_palindrome(self, text: str) -> bool:
        """Check if the given text is a palindrome."""
        pass


class CaseSensitivity(Enum):
    """Enumeration for case sensitivity options."""
    SENSITIVE = "sensitive"
    INSENSITIVE = "insensitive"


class CharacterFilter(Enum):
    """Enumeration for character filtering options."""
    ALL = "all"
    ALPHANUMERIC_ONLY = "alphanumeric_only"


@runtime_checkable
class TextNormalizer(Protocol):
    """Protocol for text normalization strategies."""
    
    def normalize(self, text: str) -> str:
        """Normalize the input text according to specific rules."""
        ...


class StandardTextNormalizer:
    """Standard text normalizer that handles case and character filtering."""
    
    def __init__(self, 
                 case_sensitivity: CaseSensitivity = CaseSensitivity.INSENSITIVE,
                 character_filter: CharacterFilter = CharacterFilter.ALPHANUMERIC_ONLY):
        self._case_sensitivity = case_sensitivity
        self._character_filter = character_filter
    
    def normalize(self, text: str) -> str:
        """Normalize text based on configured options."""
        normalized = text
        
        if self._case_sensitivity == CaseSensitivity.INSENSITIVE:
            normalized = normalized.lower()
        
        if self._character_filter == CharacterFilter.ALPHANUMERIC_ONLY:
            normalized = re.sub(r'[^a-zA-Z0-9]', '', normalized)
        
        return normalized


class TwoPointerPalindromeStrategy(PalindromeStrategy):
    """Two-pointer algorithm strategy for palindrome checking."""
    
    def __init__(self, normalizer: TextNormalizer):
        self._normalizer = normalizer
    
    def is_palindrome(self, text: str) -> bool:
        """Check palindrome using two-pointer technique."""
        normalized = self._normalizer.normalize(text)
        
        if not normalized:
            return True  # Empty string is considered a palindrome
        
        left, right = 0, len(normalized) - 1
        
        while left < right:
            if normalized[left] != normalized[right]:
                return False
            left += 1
            right -= 1
        
        return True


class ReversalPalindromeStrategy(PalindromeStrategy):
    """String reversal strategy for palindrome checking."""
    
    def __init__(self, normalizer: TextNormalizer):
        self._normalizer = normalizer
    
    def is_palindrome(self, text: str) -> bool:
        """Check palindrome by comparing with reversed string."""
        normalized = self._normalizer.normalize(text)
        return normalized == normalized[::-1]


class RecursivePalindromeStrategy(PalindromeStrategy):
    """Recursive strategy for palindrome checking."""
    
    def __init__(self, normalizer: TextNormalizer):
        self._normalizer = normalizer
    
    def is_palindrome(self, text: str) -> bool:
        """Check palindrome using recursive approach."""
        normalized = self._normalizer.normalize(text)
        return self._is_palindrome_recursive(normalized)
    
    def _is_palindrome_recursive(self, text: str) -> bool:
        """Recursive helper method."""
        if len(text) <= 1:
            return True
        
        if text[0] != text[-1]:
            return False
        
        return self._is_palindrome_recursive(text[1:-1])


class PalindromeStrategyFactory:
    """Factory for creating palindrome checking strategies."""
    
    @staticmethod
    def create_strategy(strategy_type: str, normalizer: TextNormalizer) -> PalindromeStrategy:
        """Create a palindrome strategy based on the specified type."""
        strategies = {
            'two_pointer': TwoPointerPalindromeStrategy,
            'reversal': ReversalPalindromeStrategy,
            'recursive': RecursivePalindromeStrategy
        }
        
        strategy_class = strategies.get(strategy_type.lower())
        if not strategy_class:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
        
        return strategy_class(normalizer)


class PalindromeChecker:
    """Main palindrome checker class that uses the Strategy pattern."""
    
    def __init__(self, strategy: PalindromeStrategy):
        self._strategy = strategy
    
    def check(self, text: str) -> bool:
        """Check if the given text is a palindrome."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        return self._strategy.is_palindrome(text)
    
    def set_strategy(self, strategy: PalindromeStrategy) -> None:
        """Change the palindrome checking strategy at runtime."""
        self._strategy = strategy


class PalindromeCheckerBuilder:
    """Builder pattern for creating configured palindrome checkers."""
    
    def __init__(self):
        self._strategy_type = 'two_pointer'
        self._case_sensitivity = CaseSensitivity.INSENSITIVE
        self._character_filter = CharacterFilter.ALPHANUMERIC_ONLY
    
    def with_strategy(self, strategy_type: str) -> 'PalindromeCheckerBuilder':
        """Set the palindrome checking strategy."""
        self._strategy_type = strategy_type
        return self
    
    def with_case_sensitivity(self, case_sensitivity: CaseSensitivity) -> 'PalindromeCheckerBuilder':
        """Set case sensitivity option."""
        self._case_sensitivity = case_sensitivity
        return self
    
    def with_character_filter(self, character_filter: CharacterFilter) -> 'PalindromeCheckerBuilder':
        """Set character filtering option."""
        self._character_filter = character_filter
        return self
    
    def build(self) -> PalindromeChecker:
        """Build the configured palindrome checker."""
        normalizer = StandardTextNormalizer(self._case_sensitivity, self._character_filter)
        strategy = PalindromeStrategyFactory.create_strategy(self._strategy_type, normalizer)
        return PalindromeChecker(strategy)


# Convenience function with default configuration
def is_palindrome(text: str) -> bool:
    """
    Simple function to check if a string is a palindrome using default settings.
    
    Args:
        text: The string to check
        
    Returns:
        bool: True if the string is a palindrome, False otherwise
        
    Raises:
        TypeError: If input is not a string
    """
    checker = (PalindromeCheckerBuilder()
               .with_strategy('two_pointer')
               .with_case_sensitivity(CaseSensitivity.INSENSITIVE)
               .with_character_filter(CharacterFilter.ALPHANUMERIC_ONLY)
               .build())
    
    return checker.check(text)


# Example usage and demonstration
if __name__ == "__main__":
    # Simple usage with convenience function
    print(is_palindrome("A man, a plan, a canal: Panama"))  # True
    print(is_palindrome("race a car"))  # False
    
    # Advanced usage with custom configuration
    strict_checker = (PalindromeCheckerBuilder()
                     .with_strategy('recursive')
                     .with_case_sensitivity(CaseSensitivity.SENSITIVE)
                     .with_character_filter(CharacterFilter.ALL)
                     .build())
    
    print(strict_checker.check("Aa"))  # False (case sensitive)
    
    # Runtime strategy switching
    checker = (PalindromeCheckerBuilder()
              .with_strategy('reversal')
              .build())
    
    print(checker.check("racecar"))  # True
    
    # Switch to different strategy
    normalizer = StandardTextNormalizer()
    new_strategy = TwoPointerPalindromeStrategy(normalizer)
    checker.set_strategy(new_strategy)
    print(checker.check("Was it a car or a cat I saw?"))  # True
```

This implementation demonstrates several design patterns and architectural principles:

## Design Patterns Used:

1. **Strategy Pattern**: Different algorithms for palindrome checking (two-pointer, reversal, recursive)
2. **Factory Pattern**: `PalindromeStrategyFactory` creates appropriate strategy instances
3. **Builder Pattern**: `PalindromeCheckerBuilder` for flexible configuration
4. **Protocol/Interface Segregation**: `TextNormalizer` protocol and `PalindromeStrategy` abstract base class

## SOLID Principles:

1. **Single Responsibility**: Each class has one clear purpose
2. **Open/Closed**: Easy to add new strategies without modifying existing code
3. **Liskov Substitution**: All strategies are interchangeable
4. **Interface Segregation**: Clean, focused interfaces
5. **Dependency Inversion**: High-level classes depend on abstractions

## Key Features:

- **Extensibility**: Easy to add new palindrome algorithms or normalization strategies
- **Configurability**: Flexible options for case sensitivity and character filtering
- **Runtime Strategy Switching**: Can change algorithms dynamically
- **Type Safety**: Proper type hints and runtime checking
- **Error Handling**: Appropriate exception handling
- **Clean API**: Both simple function and advanced class-based interfaces

This architecture makes the code maintainable, testable, and extensible while providing a clean, easy-to-use interface.