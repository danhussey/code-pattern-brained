# User Validator - Pattern Brained

**Prompt:** Write code to validate user registration data: email must be valid format, password must be at least 8 characters with a number, username must be alphanumeric.

**Output tokens:** 2625

## Response

I'll create a well-architected user registration validation system using proper design patterns and SOLID principles.

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Protocol
from dataclasses import dataclass
from enum import Enum
import re


class ValidationResult:
    """Value object to encapsulate validation results"""
    
    def __init__(self, is_valid: bool = True, errors: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
    
    def add_error(self, error: str) -> None:
        self.errors.append(error)
        self.is_valid = False
    
    def merge(self, other: 'ValidationResult') -> 'ValidationResult':
        """Merge two validation results"""
        combined_errors = self.errors + other.errors
        return ValidationResult(
            is_valid=self.is_valid and other.is_valid,
            errors=combined_errors
        )


@dataclass
class UserRegistrationData:
    """Data Transfer Object for user registration"""
    email: str
    password: str
    username: str


class ValidationError(Exception):
    """Custom exception for validation errors"""
    
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__(f"Validation failed: {', '.join(errors)}")


class IValidator(Protocol):
    """Interface for all validators using Protocol (duck typing)"""
    
    def validate(self, value: str) -> ValidationResult:
        """Validate a value and return validation result"""
        ...


class BaseValidator(ABC):
    """Abstract base class for validators implementing Template Method pattern"""
    
    @abstractmethod
    def _perform_validation(self, value: str) -> ValidationResult:
        """Concrete validation logic to be implemented by subclasses"""
        pass
    
    def validate(self, value: str) -> ValidationResult:
        """Template method that defines the validation algorithm"""
        if not isinstance(value, str):
            return ValidationResult(False, ["Value must be a string"])
        
        if not value or not value.strip():
            return ValidationResult(False, ["Value cannot be empty"])
        
        return self._perform_validation(value.strip())


class EmailValidator(BaseValidator):
    """Validator for email format using regex strategy"""
    
    def __init__(self, pattern: str = None):
        # Strategy pattern: allow different email validation patterns
        self._pattern = pattern or r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        self._regex = re.compile(self._pattern)
    
    def _perform_validation(self, value: str) -> ValidationResult:
        if not self._regex.match(value):
            return ValidationResult(False, ["Invalid email format"])
        return ValidationResult()


class PasswordValidator(BaseValidator):
    """Validator for password strength with configurable rules"""
    
    def __init__(self, min_length: int = 8, require_number: bool = True):
        self._min_length = min_length
        self._require_number = require_number
    
    def _perform_validation(self, value: str) -> ValidationResult:
        result = ValidationResult()
        
        if len(value) < self._min_length:
            result.add_error(f"Password must be at least {self._min_length} characters long")
        
        if self._require_number and not re.search(r'\d', value):
            result.add_error("Password must contain at least one number")
        
        return result


class UsernameValidator(BaseValidator):
    """Validator for alphanumeric username"""
    
    def __init__(self, min_length: int = 1, max_length: int = 50):
        self._min_length = min_length
        self._max_length = max_length
        self._pattern = re.compile(r'^[a-zA-Z0-9]+$')
    
    def _perform_validation(self, value: str) -> ValidationResult:
        result = ValidationResult()
        
        if len(value) < self._min_length:
            result.add_error(f"Username must be at least {self._min_length} characters long")
        
        if len(value) > self._max_length:
            result.add_error(f"Username cannot exceed {self._max_length} characters")
        
        if not self._pattern.match(value):
            result.add_error("Username must contain only alphanumeric characters")
        
        return result


class ValidatorFactory:
    """Factory pattern for creating validators"""
    
    _validators = {
        'email': EmailValidator,
        'password': PasswordValidator,
        'username': UsernameValidator,
    }
    
    @classmethod
    def create_validator(cls, validator_type: str, **kwargs) -> IValidator:
        if validator_type not in cls._validators:
            raise ValueError(f"Unknown validator type: {validator_type}")
        
        return cls._validators[validator_type](**kwargs)
    
    @classmethod
    def register_validator(cls, name: str, validator_class: type) -> None:
        """Allow registration of custom validators"""
        cls._validators[name] = validator_class


class UserRegistrationValidator:
    """Main validator class using Composite pattern to combine multiple validators"""
    
    def __init__(self, 
                 email_validator: IValidator = None,
                 password_validator: IValidator = None,
                 username_validator: IValidator = None):
        # Dependency injection for flexibility and testability
        self._email_validator = email_validator or ValidatorFactory.create_validator('email')
        self._password_validator = password_validator or ValidatorFactory.create_validator('password')
        self._username_validator = username_validator or ValidatorFactory.create_validator('username')
    
    def validate(self, user_data: UserRegistrationData) -> ValidationResult:
        """Validate all user registration data"""
        email_result = self._email_validator.validate(user_data.email)
        password_result = self._password_validator.validate(user_data.password)
        username_result = self._username_validator.validate(user_data.username)
        
        # Combine all validation results
        return email_result.merge(password_result).merge(username_result)
    
    def validate_and_raise(self, user_data: UserRegistrationData) -> None:
        """Validate and raise exception if invalid"""
        result = self.validate(user_data)
        if not result.is_valid:
            raise ValidationError(result.errors)


class UserRegistrationService:
    """Service class that uses the validator - demonstrates Dependency Inversion"""
    
    def __init__(self, validator: UserRegistrationValidator = None):
        self._validator = validator or UserRegistrationValidator()
    
    def register_user(self, email: str, password: str, username: str) -> Dict[str, Any]:
        """Register a user after validation"""
        user_data = UserRegistrationData(
            email=email,
            password=password,
            username=username
        )
        
        validation_result = self._validator.validate(user_data)
        
        if not validation_result.is_valid:
            return {
                'success': False,
                'errors': validation_result.errors
            }
        
        # Here you would typically save to database
        return {
            'success': True,
            'message': 'User registered successfully',
            'user_data': {
                'email': user_data.email,
                'username': user_data.username
                # Note: never return password in response
            }
        }


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Basic usage
    service = UserRegistrationService()
    
    # Valid registration
    result1 = service.register_user(
        email="user@example.com",
        password="password123",
        username="john_doe"  # This will fail - contains underscore
    )
    print("Result 1:", result1)
    
    # Valid registration
    result2 = service.register_user(
        email="user@example.com",
        password="password123",
        username="johndoe"
    )
    print("Result 2:", result2)
    
    # Example 2: Custom validator configuration
    custom_password_validator = ValidatorFactory.create_validator(
        'password', 
        min_length=12, 
        require_number=True
    )
    
    custom_validator = UserRegistrationValidator(
        password_validator=custom_password_validator
    )
    
    custom_service = UserRegistrationService(validator=custom_validator)
    
    result3 = custom_service.register_user(
        email="user@example.com",
        password="short",  # Will fail custom length requirement
        username="johndoe"
    )
    print("Result 3:", result3)
    
    # Example 3: Using validation directly
    validator = UserRegistrationValidator()
    user_data = UserRegistrationData(
        email="invalid-email",
        password="weak",
        username="user@123"  # Contains @ symbol
    )
    
    validation_result = validator.validate(user_data)
    print(f"Is valid: {validation_result.is_valid}")
    print(f"Errors: {validation_result.errors}")
```

This implementation demonstrates several key design patterns and principles:

## Design Patterns Used:

1. **Strategy Pattern**: Different validation strategies can be plugged in
2. **Factory Pattern**: `ValidatorFactory` creates validators
3. **Template Method Pattern**: `BaseValidator` defines the validation algorithm structure
4. **Composite Pattern**: `UserRegistrationValidator` combines multiple validators
5. **Dependency Injection**: Services accept validators as dependencies

## SOLID Principles:

1. **Single Responsibility**: Each validator handles one type of validation
2. **Open/Closed**: Easy to add new validators without modifying existing code
3. **Liskov Substitution**: All validators can be used interchangeably
4. **Interface Segregation**: Clean, focused interfaces
5. **Dependency Inversion**: High-level modules depend on abstractions

## Key Features:

- **Extensible**: Easy to add new validation rules
- **Configurable**: Validators accept configuration parameters
- **Testable**: Dependencies can be mocked
- **Reusable**: Validators can be used independently
- **Error Handling**: Comprehensive error collection and reporting
- **Type Safety**: Uses type hints and protocols

This architecture makes the code maintainable, testable, and easily extensible for future requirements.