# Calculator - Pattern Brained

**Prompt:** Write a calculator that supports add, subtract, multiply, and divide operations.

**Output tokens:** 2993

## Response

I'll create a well-architected calculator using proper design patterns and SOLID principles. Here's my implementation:

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Type
from decimal import Decimal, InvalidOperation


class OperationType(Enum):
    """Enumeration of supported operation types."""
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculatorError(Exception):
    """Base exception for calculator-related errors."""
    pass


class InvalidOperationError(CalculatorError):
    """Raised when an invalid operation is requested."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class InvalidInputError(CalculatorError):
    """Raised when invalid input is provided."""
    pass


class Operation(ABC):
    """Abstract base class for mathematical operations."""
    
    @abstractmethod
    def execute(self, left_operand: Decimal, right_operand: Decimal) -> Decimal:
        """Execute the operation on two operands.
        
        Args:
            left_operand: The left operand
            right_operand: The right operand
            
        Returns:
            The result of the operation
            
        Raises:
            CalculatorError: If the operation cannot be performed
        """
        pass
    
    @property
    @abstractmethod
    def symbol(self) -> str:
        """Return the symbol representing this operation."""
        pass


class AddOperation(Operation):
    """Implementation of addition operation."""
    
    def execute(self, left_operand: Decimal, right_operand: Decimal) -> Decimal:
        return left_operand + right_operand
    
    @property
    def symbol(self) -> str:
        return "+"


class SubtractOperation(Operation):
    """Implementation of subtraction operation."""
    
    def execute(self, left_operand: Decimal, right_operand: Decimal) -> Decimal:
        return left_operand - right_operand
    
    @property
    def symbol(self) -> str:
        return "-"


class MultiplyOperation(Operation):
    """Implementation of multiplication operation."""
    
    def execute(self, left_operand: Decimal, right_operand: Decimal) -> Decimal:
        return left_operand * right_operand
    
    @property
    def symbol(self) -> str:
        return "*"


class DivideOperation(Operation):
    """Implementation of division operation."""
    
    def execute(self, left_operand: Decimal, right_operand: Decimal) -> Decimal:
        if right_operand == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return left_operand / right_operand
    
    @property
    def symbol(self) -> str:
        return "/"


class OperationFactory:
    """Factory class for creating operation instances."""
    
    _operation_registry: Dict[OperationType, Type[Operation]] = {
        OperationType.ADD: AddOperation,
        OperationType.SUBTRACT: SubtractOperation,
        OperationType.MULTIPLY: MultiplyOperation,
        OperationType.DIVIDE: DivideOperation,
    }
    
    @classmethod
    def create_operation(cls, operation_type: OperationType) -> Operation:
        """Create an operation instance based on the operation type.
        
        Args:
            operation_type: The type of operation to create
            
        Returns:
            An instance of the requested operation
            
        Raises:
            InvalidOperationError: If the operation type is not supported
        """
        if operation_type not in cls._operation_registry:
            raise InvalidOperationError(f"Unsupported operation: {operation_type}")
        
        operation_class = cls._operation_registry[operation_type]
        return operation_class()
    
    @classmethod
    def register_operation(cls, operation_type: OperationType, 
                          operation_class: Type[Operation]) -> None:
        """Register a new operation type (for extensibility).
        
        Args:
            operation_type: The operation type to register
            operation_class: The operation class to associate with the type
        """
        cls._operation_registry[operation_type] = operation_class
    
    @classmethod
    def get_supported_operations(cls) -> list[OperationType]:
        """Get a list of all supported operation types."""
        return list(cls._operation_registry.keys())


class InputValidator:
    """Validator for calculator inputs."""
    
    @staticmethod
    def validate_numeric_input(value: str) -> Decimal:
        """Validate and convert string input to Decimal.
        
        Args:
            value: String representation of a number
            
        Returns:
            Decimal representation of the input
            
        Raises:
            InvalidInputError: If the input is not a valid number
        """
        try:
            return Decimal(str(value).strip())
        except (InvalidOperation, ValueError) as e:
            raise InvalidInputError(f"Invalid numeric input: {value}") from e


class CalculationResult:
    """Data class representing the result of a calculation."""
    
    def __init__(self, left_operand: Decimal, operation_symbol: str, 
                 right_operand: Decimal, result: Decimal):
        self.left_operand = left_operand
        self.operation_symbol = operation_symbol
        self.right_operand = right_operand
        self.result = result
    
    def __str__(self) -> str:
        return f"{self.left_operand} {self.operation_symbol} {self.right_operand} = {self.result}"
    
    def __repr__(self) -> str:
        return (f"CalculationResult(left_operand={self.left_operand}, "
                f"operation_symbol='{self.operation_symbol}', "
                f"right_operand={self.right_operand}, result={self.result})")


class Calculator:
    """Main calculator class that orchestrates operations."""
    
    def __init__(self, operation_factory: OperationFactory = None,
                 input_validator: InputValidator = None):
        """Initialize the calculator with dependencies.
        
        Args:
            operation_factory: Factory for creating operations (dependency injection)
            input_validator: Validator for inputs (dependency injection)
        """
        self._operation_factory = operation_factory or OperationFactory()
        self._input_validator = input_validator or InputValidator()
    
    def calculate(self, left_operand: str, operation_type: OperationType, 
                 right_operand: str) -> CalculationResult:
        """Perform a calculation.
        
        Args:
            left_operand: String representation of the left operand
            operation_type: The type of operation to perform
            right_operand: String representation of the right operand
            
        Returns:
            CalculationResult containing the operation details and result
            
        Raises:
            CalculatorError: If the calculation cannot be performed
        """
        # Validate inputs
        left_decimal = self._input_validator.validate_numeric_input(left_operand)
        right_decimal = self._input_validator.validate_numeric_input(right_operand)
        
        # Create and execute operation
        operation = self._operation_factory.create_operation(operation_type)
        result = operation.execute(left_decimal, right_decimal)
        
        # Return structured result
        return CalculationResult(
            left_operand=left_decimal,
            operation_symbol=operation.symbol,
            right_operand=right_decimal,
            result=result
        )
    
    def get_supported_operations(self) -> list[OperationType]:
        """Get list of supported operations."""
        return self._operation_factory.get_supported_operations()


class CalculatorInterface:
    """Command-line interface for the calculator."""
    
    def __init__(self, calculator: Calculator = None):
        """Initialize the interface.
        
        Args:
            calculator: Calculator instance (dependency injection)
        """
        self._calculator = calculator or Calculator()
    
    def run_interactive_session(self) -> None:
        """Run an interactive calculator session."""
        print("Welcome to the Calculator!")
        print("Supported operations: add, subtract, multiply, divide")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                # Get user input
                left = input("Enter first number: ").strip()
                if left.lower() == 'quit':
                    break
                
                operation = input("Enter operation (add/subtract/multiply/divide): ").strip()
                if operation.lower() == 'quit':
                    break
                
                right = input("Enter second number: ").strip()
                if right.lower() == 'quit':
                    break
                
                # Map string to operation type
                operation_mapping = {
                    'add': OperationType.ADD,
                    'subtract': OperationType.SUBTRACT,
                    'multiply': OperationType.MULTIPLY,
                    'divide': OperationType.DIVIDE
                }
                
                if operation.lower() not in operation_mapping:
                    print(f"Error: Unsupported operation '{operation}'\n")
                    continue
                
                operation_type = operation_mapping[operation.lower()]
                
                # Perform calculation
                result = self._calculator.calculate(left, operation_type, right)
                print(f"Result: {result}\n")
                
            except CalculatorError as e:
                print(f"Calculator Error: {e}\n")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Unexpected error: {e}\n")


# Example usage and demonstration
if __name__ == "__main__":
    # Example of direct usage
    calc = Calculator()
    
    try:
        # Perform some calculations
        result1 = calc.calculate("10", OperationType.ADD, "5")
        print(result1)  # 10 + 5 = 15
        
        result2 = calc.calculate("20.5", OperationType.MULTIPLY, "3")
        print(result2)  # 20.5 * 3 = 61.5
        
        result3 = calc.calculate("15", OperationType.DIVIDE, "3")
        print(result3)  # 15 / 3 = 5
        
    except CalculatorError as e:
        print(f"Error: {e}")
    
    # Run interactive session (uncomment to test)
    # interface = CalculatorInterface(calc)
    # interface.run_interactive_session()
```

This implementation demonstrates several key design principles and patterns:

## Design Patterns Used:

1. **Strategy Pattern**: The `Operation` abstract base class with concrete implementations
2. **Factory Pattern**: `OperationFactory` for creating operation instances
3. **Dependency Injection**: Calculator accepts factory and validator dependencies
4. **Command Pattern**: Operations encapsulate calculations as executable commands

## SOLID Principles:

1. **Single Responsibility**: Each class has one clear purpose
2. **Open/Closed**: Easy to add new operations without modifying existing code
3. **Liskov Substitution**: All operations can be used interchangeably
4. **Interface Segregation**: Clean, focused interfaces
5. **Dependency Inversion**: Calculator depends on abstractions, not concretions

## Key Features:

- **Extensibility**: Easy to add new operations by implementing `Operation` interface
- **Error Handling**: Comprehensive exception hierarchy for different error types
- **Input Validation**: Robust validation using `Decimal` for precision
- **Separation of Concerns**: UI, business logic, and data validation are separate
- **Type Safety**: Full type hints and enums for better IDE support
- **Testability**: All dependencies can be mocked for unit testing

The calculator can be used programmatically or through the interactive interface, and new operations can be easily added by extending the `Operation` base class and registering them with the factory.