# FizzBuzz - Pattern Brained

**Prompt:** Write a function that prints numbers from 1 to 100. For multiples of 3, print 'Fizz'. For multiples of 5, print 'Buzz'. For multiples of both, print 'FizzBuzz'.

**Output tokens:** 1839

## Response

I'll implement the FizzBuzz problem using proper software architecture principles with design patterns and SOLID principles.

```python
from abc import ABC, abstractmethod
from typing import List, Dict
from dataclasses import dataclass


class Rule(ABC):
    """Abstract base class for FizzBuzz rules following Strategy pattern."""
    
    @abstractmethod
    def applies(self, number: int) -> bool:
        """Check if this rule applies to the given number."""
        pass
    
    @abstractmethod
    def get_output(self) -> str:
        """Get the output string for this rule."""
        pass


class DivisibilityRule(Rule):
    """Concrete rule for divisibility-based conditions."""
    
    def __init__(self, divisor: int, output: str):
        self._divisor = divisor
        self._output = output
    
    def applies(self, number: int) -> bool:
        return number % self._divisor == 0
    
    def get_output(self) -> str:
        return self._output


class CompositeRule(Rule):
    """Composite rule that combines multiple rules using AND logic."""
    
    def __init__(self, rules: List[Rule], output: str):
        self._rules = rules
        self._output = output
    
    def applies(self, number: int) -> bool:
        return all(rule.applies(number) for rule in self._rules)
    
    def get_output(self) -> str:
        return self._output


@dataclass
class NumberRange:
    """Value object representing a range of numbers."""
    start: int
    end: int
    
    def __post_init__(self):
        if self.start > self.end:
            raise ValueError("Start must be less than or equal to end")


class RuleEngine:
    """Engine that processes numbers against a set of rules."""
    
    def __init__(self):
        self._rules: List[Rule] = []
    
    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the engine. Rules are evaluated in order of addition."""
        self._rules.append(rule)
    
    def process_number(self, number: int) -> str:
        """Process a number against all rules, returning the first match or the number itself."""
        for rule in self._rules:
            if rule.applies(number):
                return rule.get_output()
        return str(number)


class OutputWriter(ABC):
    """Abstract base class for output writers following Strategy pattern."""
    
    @abstractmethod
    def write(self, content: str) -> None:
        pass


class ConsoleWriter(OutputWriter):
    """Concrete writer that outputs to console."""
    
    def write(self, content: str) -> None:
        print(content)


class FizzBuzzRuleFactory:
    """Factory for creating standard FizzBuzz rules."""
    
    @staticmethod
    def create_standard_rules() -> List[Rule]:
        """Create the standard FizzBuzz rules."""
        fizz_rule = DivisibilityRule(3, "Fizz")
        buzz_rule = DivisibilityRule(5, "Buzz")
        fizzbuzz_rule = CompositeRule([fizz_rule, buzz_rule], "FizzBuzz")
        
        # Order matters: more specific rules first
        return [fizzbuzz_rule, fizz_rule, buzz_rule]


class FizzBuzzGame:
    """Main game class that orchestrates the FizzBuzz logic."""
    
    def __init__(self, rule_engine: RuleEngine, output_writer: OutputWriter):
        self._rule_engine = rule_engine
        self._output_writer = output_writer
    
    def play(self, number_range: NumberRange) -> None:
        """Play the FizzBuzz game for the given range."""
        for number in range(number_range.start, number_range.end + 1):
            result = self._rule_engine.process_number(number)
            self._output_writer.write(result)


class FizzBuzzGameBuilder:
    """Builder pattern for constructing FizzBuzz game instances."""
    
    def __init__(self):
        self._rule_engine = RuleEngine()
        self._output_writer: OutputWriter = ConsoleWriter()
    
    def with_standard_rules(self) -> 'FizzBuzzGameBuilder':
        """Add standard FizzBuzz rules."""
        rules = FizzBuzzRuleFactory.create_standard_rules()
        for rule in rules:
            self._rule_engine.add_rule(rule)
        return self
    
    def with_custom_rule(self, rule: Rule) -> 'FizzBuzzGameBuilder':
        """Add a custom rule."""
        self._rule_engine.add_rule(rule)
        return self
    
    def with_output_writer(self, writer: OutputWriter) -> 'FizzBuzzGameBuilder':
        """Set custom output writer."""
        self._output_writer = writer
        return self
    
    def build(self) -> FizzBuzzGame:
        """Build the FizzBuzz game instance."""
        return FizzBuzzGame(self._rule_engine, self._output_writer)


def main():
    """Main function demonstrating the FizzBuzz implementation."""
    # Build and configure the game
    game = (FizzBuzzGameBuilder()
            .with_standard_rules()
            .build())
    
    # Define the range
    number_range = NumberRange(1, 100)
    
    # Play the game
    game.play(number_range)


# Example of extending the system with custom rules
def example_with_custom_rules():
    """Example showing how to extend the system with custom rules."""
    
    # Create custom rules
    seven_rule = DivisibilityRule(7, "Lucky")
    eleven_rule = DivisibilityRule(11, "Boom")
    
    # Build game with custom rules
    game = (FizzBuzzGameBuilder()
            .with_standard_rules()
            .with_custom_rule(seven_rule)
            .with_custom_rule(eleven_rule)
            .build())
    
    # Play with custom range
    game.play(NumberRange(1, 30))


if __name__ == "__main__":
    main()
```

This implementation demonstrates several key design patterns and architectural principles:

## Design Patterns Used:

1. **Strategy Pattern**: `Rule` hierarchy allows different rule implementations
2. **Composite Pattern**: `CompositeRule` combines multiple rules
3. **Factory Pattern**: `FizzBuzzRuleFactory` creates standard rule sets
4. **Builder Pattern**: `FizzBuzzGameBuilder` constructs game instances
5. **Template Method**: Abstract base classes define structure

## SOLID Principles:

1. **Single Responsibility**: Each class has one clear purpose
2. **Open/Closed**: Easy to add new rules without modifying existing code
3. **Liskov Substitution**: All rule implementations are interchangeable
4. **Interface Segregation**: Clean, focused interfaces
5. **Dependency Inversion**: Depends on abstractions, not concretions

## Key Features:

- **Extensible**: Easy to add new rules or output formats
- **Testable**: Each component can be unit tested independently  
- **Maintainable**: Clear separation of concerns
- **Configurable**: Rules and output can be customized
- **Type Safe**: Proper type hints throughout
- **Error Handling**: Input validation where appropriate

The architecture makes it trivial to extend (add new rules, output formats) while maintaining the existing functionality intact.