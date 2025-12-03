# Fibonacci - Pattern Brained

**Prompt:** Write a function that returns the nth Fibonacci number.

**Output tokens:** 2660

## Response

I'll create a well-architected Fibonacci calculator using proper design patterns and SOLID principles.

```python
from abc import ABC, abstractmethod
from typing import Dict, Optional
from functools import wraps
import threading


class FibonacciStrategy(ABC):
    """Strategy interface for different Fibonacci calculation algorithms."""
    
    @abstractmethod
    def calculate(self, n: int) -> int:
        """Calculate the nth Fibonacci number."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the strategy name."""
        pass


class MemoizedFibonacciStrategy(FibonacciStrategy):
    """Memoized recursive strategy for Fibonacci calculation."""
    
    def __init__(self):
        self._cache: Dict[int, int] = {0: 0, 1: 1}
        self._lock = threading.RLock()
    
    def calculate(self, n: int) -> int:
        """Calculate using memoized recursion."""
        if n < 0:
            raise ValueError("Fibonacci number is not defined for negative integers")
        
        with self._lock:
            if n in self._cache:
                return self._cache[n]
            
            result = self.calculate(n - 1) + self.calculate(n - 2)
            self._cache[n] = result
            return result
    
    @property
    def name(self) -> str:
        return "Memoized Recursive"


class IterativeFibonacciStrategy(FibonacciStrategy):
    """Iterative strategy for Fibonacci calculation."""
    
    def calculate(self, n: int) -> int:
        """Calculate using iterative approach."""
        if n < 0:
            raise ValueError("Fibonacci number is not defined for negative integers")
        
        if n <= 1:
            return n
        
        prev, curr = 0, 1
        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr
        
        return curr
    
    @property
    def name(self) -> str:
        return "Iterative"


class MatrixFibonacciStrategy(FibonacciStrategy):
    """Matrix exponentiation strategy for Fibonacci calculation."""
    
    def calculate(self, n: int) -> int:
        """Calculate using matrix exponentiation."""
        if n < 0:
            raise ValueError("Fibonacci number is not defined for negative integers")
        
        if n <= 1:
            return n
        
        def matrix_multiply(a: list, b: list) -> list:
            """Multiply two 2x2 matrices."""
            return [
                [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
                [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]
            ]
        
        def matrix_power(matrix: list, power: int) -> list:
            """Calculate matrix to the power using binary exponentiation."""
            if power == 1:
                return matrix
            
            result = [[1, 0], [0, 1]]  # Identity matrix
            base = matrix
            
            while power > 0:
                if power % 2 == 1:
                    result = matrix_multiply(result, base)
                base = matrix_multiply(base, base)
                power //= 2
            
            return result
        
        base_matrix = [[1, 1], [1, 0]]
        result_matrix = matrix_power(base_matrix, n)
        return result_matrix[0][1]
    
    @property
    def name(self) -> str:
        return "Matrix Exponentiation"


class FibonacciStrategyFactory:
    """Factory for creating Fibonacci calculation strategies."""
    
    _strategies = {
        'memoized': MemoizedFibonacciStrategy,
        'iterative': IterativeFibonacciStrategy,
        'matrix': MatrixFibonacciStrategy
    }
    
    @classmethod
    def create_strategy(cls, strategy_type: str) -> FibonacciStrategy:
        """Create a strategy instance."""
        if strategy_type not in cls._strategies:
            raise ValueError(f"Unknown strategy: {strategy_type}. "
                           f"Available strategies: {list(cls._strategies.keys())}")
        
        return cls._strategies[strategy_type]()
    
    @classmethod
    def get_available_strategies(cls) -> list:
        """Get list of available strategy names."""
        return list(cls._strategies.keys())


class FibonacciCalculator:
    """Main calculator class that uses the Strategy pattern."""
    
    def __init__(self, strategy: Optional[FibonacciStrategy] = None):
        self._strategy = strategy or IterativeFibonacciStrategy()
    
    def set_strategy(self, strategy: FibonacciStrategy) -> None:
        """Set the calculation strategy."""
        self._strategy = strategy
    
    def calculate(self, n: int) -> int:
        """Calculate the nth Fibonacci number using the current strategy."""
        return self._strategy.calculate(n)
    
    @property
    def current_strategy(self) -> str:
        """Get the name of the current strategy."""
        return self._strategy.name


class FibonacciService:
    """Service class that provides a high-level interface."""
    
    def __init__(self):
        self._calculator = FibonacciCalculator()
        self._factory = FibonacciStrategyFactory()
    
    def get_fibonacci(self, n: int, strategy: str = 'iterative') -> int:
        """
        Get the nth Fibonacci number using the specified strategy.
        
        Args:
            n: The position in the Fibonacci sequence
            strategy: The calculation strategy ('memoized', 'iterative', 'matrix')
            
        Returns:
            The nth Fibonacci number
            
        Raises:
            ValueError: If n is negative or strategy is unknown
        """
        fibonacci_strategy = self._factory.create_strategy(strategy)
        self._calculator.set_strategy(fibonacci_strategy)
        return self._calculator.calculate(n)
    
    def get_available_strategies(self) -> list:
        """Get list of available calculation strategies."""
        return self._factory.get_available_strategies()


# Singleton pattern for global access (if needed)
class FibonacciServiceSingleton:
    """Singleton wrapper for FibonacciService."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._service = FibonacciService()
        return cls._instance
    
    def get_fibonacci(self, n: int, strategy: str = 'iterative') -> int:
        """Get the nth Fibonacci number."""
        return self._service.get_fibonacci(n, strategy)
    
    def get_available_strategies(self) -> list:
        """Get available strategies."""
        return self._service.get_available_strategies()


# Convenient function interface
def fibonacci(n: int, strategy: str = 'iterative') -> int:
    """
    Calculate the nth Fibonacci number.
    
    This is a convenient function interface that uses the well-architected
    classes behind the scenes.
    
    Args:
        n: The position in the Fibonacci sequence (0-indexed)
        strategy: Calculation strategy ('iterative', 'memoized', 'matrix')
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative or strategy is unknown
        
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(10)
        55
        >>> fibonacci(10, strategy='matrix')
        55
    """
    service = FibonacciService()
    return service.get_fibonacci(n, strategy)


# Example usage and testing
if __name__ == "__main__":
    # Test the function interface
    print("Testing function interface:")
    for i in range(10):
        print(f"F({i}) = {fibonacci(i)}")
    
    # Test different strategies
    print(f"\nF(20) with different strategies:")
    service = FibonacciService()
    n = 20
    
    for strategy in service.get_available_strategies():
        result = service.get_fibonacci(n, strategy)
        print(f"Strategy '{strategy}': F({n}) = {result}")
    
    # Test error handling
    try:
        fibonacci(-1)
    except ValueError as e:
        print(f"\nError handling test: {e}")
    
    # Performance test for large numbers
    print(f"\nPerformance test F(1000):")
    import time
    
    for strategy in ['iterative', 'matrix']:
        start_time = time.time()
        result = fibonacci(1000, strategy)
        end_time = time.time()
        print(f"{strategy}: {end_time - start_time:.6f} seconds")
```

This implementation demonstrates several key design patterns and architectural principles:

## Design Patterns Used:

1. **Strategy Pattern**: Different algorithms (iterative, memoized, matrix) implement the same interface
2. **Factory Pattern**: `FibonacciStrategyFactory` creates strategy instances
3. **Singleton Pattern**: `FibonacciServiceSingleton` for global access if needed

## SOLID Principles:

1. **Single Responsibility**: Each class has one clear purpose
2. **Open/Closed**: Easy to add new strategies without modifying existing code
3. **Liskov Substitution**: All strategies can be used interchangeably
4. **Interface Segregation**: Clean, focused interfaces
5. **Dependency Inversion**: High-level modules depend on abstractions

## Key Features:

- **Multiple Algorithms**: Iterative (O(n)), memoized recursive (O(n)), and matrix exponentiation (O(log n))
- **Thread Safety**: Proper locking for concurrent access
- **Error Handling**: Validates input and provides meaningful error messages
- **Extensibility**: Easy to add new calculation strategies
- **Performance**: Optimized algorithms for different use cases
- **Clean Interface**: Simple function wrapper for ease of use

The `fibonacci()` function provides a clean, simple interface while being backed by a well-architected, extensible system.