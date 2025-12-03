# I Made Claude Use Design Patterns and It Wrote 11x More Code

What happens when you tell an LLM to use design patterns "liberally"? I ran a quick experiment to find out.

## The Setup

Same model (Claude Sonnet), same problems, two different system prompts:

**Simple mode:**
> "Write the most direct, straightforward solution possible. Avoid abstractions unless absolutely necessary. If it can be done in 10 lines, don't write 100."

**Pattern-brained mode:**
> "Use established design patterns (Factory, Strategy, Observer, Singleton, etc.) where applicable. Create proper abstractions, interfaces, and base classes. Follow SOLID principles rigorously."

I ran 10 classic programming problems through both modes.

## The Results

| Problem | Pattern-Brained | Simple | Ratio |
|---------|----------------|--------|-------|
| Reverse String | 2,023 tokens | 58 tokens | **34.9x** |
| Fibonacci | 2,660 tokens | 125 tokens | **21.3x** |
| FizzBuzz | 1,839 tokens | 116 tokens | **15.9x** |
| Palindrome | 2,458 tokens | 113 tokens | **21.8x** |
| Calculator | 2,993 tokens | 282 tokens | 10.6x |
| Todo List | 3,812 tokens | 397 tokens | 9.6x |
| User Validator | 2,625 tokens | 307 tokens | 8.5x |
| File Processor | 3,461 tokens | 153 tokens | 22.6x |
| Rate Limiter | 3,756 tokens | 319 tokens | 11.8x |
| Shopping Cart | 3,717 tokens | 711 tokens | 5.2x |

**Total: 29,344 vs 2,581 tokens. 11.37x more code.**

## The Best Examples

### Reverse a String

**Simple mode:**

```python
def reverse_string(s):
    return s[::-1]
```

> "That's it. Python's slice notation `[::-1]` is the most direct way to reverse a string - no loops, no extra variables, no complexity."

**Pattern-brained mode:**

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
        return text[::-1]


class IterativeReversalStrategy:
    """Strategy implementing string reversal using iterative approach."""

    def reverse(self, text: str) -> str:
        return ''.join(reversed(text))


class RecursiveReversalStrategy:
    """Strategy implementing string reversal using recursion."""

    def reverse(self, text: str) -> str:
        if len(text) <= 1:
            return text
        return text[-1] + self.reverse(text[:-1])


class ReversalStrategyFactory:
    """Factory for creating reversal strategy instances."""
    # ... 20 more lines ...


class StringValidator:
    """Utility class for validating string inputs."""
    # ... 15 more lines ...


class StringReverser:
    """Main service class for string reversal operations."""
    # ... 25 more lines ...


class StringReversalService:
    """
    High-level service providing string reversal functionality.

    This class serves as a facade, simplifying the interface for clients
    while encapsulating the complexity of strategy selection and validation.
    """
    # ... 30 more lines ...
```

The pattern-brained version includes:
- A `ReversalStrategy` Protocol
- An enum for reversal methods
- Three different strategy implementations
- A factory to create strategies
- A validator class
- A reverser class
- A service facade
- A convenience function wrapper
- A demo script with error handling examples

All to do `s[::-1]`.

---

### FizzBuzz

**Simple mode:**

```python
def fizzbuzz():
    for i in range(1, 101):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

fizzbuzz()
```

> "That's it. Simple, direct, and does exactly what's needed."

**Pattern-brained mode:**

```python
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass


class Rule(ABC):
    """Abstract base class for FizzBuzz rules following Strategy pattern."""

    @abstractmethod
    def applies(self, number: int) -> bool:
        pass

    @abstractmethod
    def get_output(self) -> str:
        pass


class DivisibilityRule(Rule):
    """Concrete rule for divisibility-based conditions."""
    # ...


class CompositeRule(Rule):
    """Composite rule that combines multiple rules using AND logic."""
    # ...


@dataclass
class NumberRange:
    """Value object representing a range of numbers."""
    start: int
    end: int


class RuleEngine:
    """Engine that processes numbers against a set of rules."""
    # ...


class OutputWriter(ABC):
    """Abstract base class for output writers following Strategy pattern."""
    # ...


class ConsoleWriter(OutputWriter):
    """Concrete writer that outputs to console."""
    # ...


class FizzBuzzRuleFactory:
    """Factory for creating standard FizzBuzz rules."""
    # ...


class FizzBuzzGame:
    """Main game class that orchestrates the FizzBuzz logic."""
    # ...


class FizzBuzzGameBuilder:
    """Builder pattern for constructing FizzBuzz game instances."""
    # ...
```

Patterns used: Strategy, Composite, Factory, Builder, Template Method.

The response helpfully notes: *"The architecture makes it trivial to extend (add new rules, output formats) while maintaining the existing functionality intact."*

Truly, who among us hasn't needed to extend FizzBuzz with custom output formats?

## What This Means

LLMs are desperate to give you what you want, even if it isn't a very good idea. They will happily give you over-engineered code if that's what you ask for.  

It's the same in real-world software engineering, except there, it's usually managers making the dubious requests. Or, developers reach for the one size fits all solutions of SOLID and 'Clean Code' in search of best practice.

Design patterns exist because they solve real problems in large, evolving codebases. But they're tools, rather than goals. When you tell someone (or something) to use patterns "liberally," you get code that uses patterns liberally - whether they're needed or not.

The pattern-brained outputs aren't *wrong*. They're technically correct, extensible, testable, and follow SOLID principles. They're also absurd overkill for the problems at hand.

The simple outputs just... solve the problem.

## The Takeaway

If you're training or prompting a coding model, maybe don't optimize for "uses design patterns." Optimize for "solves the problem with appropriate complexity."

Or do optimize for patterns, and enjoy your `AbstractSingletonProxyFactoryBean`.

---

*Cost of this experiment: ~$0.50 in API calls.*

*Code: [github link](https://github.com/danhussey/code-pattern-brained)*
