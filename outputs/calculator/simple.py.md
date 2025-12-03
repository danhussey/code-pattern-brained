# Calculator - Simple

**Prompt:** Write a calculator that supports add, subtract, multiply, and divide operations.

**Output tokens:** 282

## Response

```python
def calculate(a, b, operation):
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        if b == 0:
            return "Error: Division by zero"
        return a / b
    else:
        return "Error: Invalid operation"

# Simple interactive calculator
while True:
    try:
        num1 = float(input("Enter first number: "))
        op = input("Enter operation (+, -, *, /) or 'q' to quit: ")
        
        if op == 'q':
            break
            
        num2 = float(input("Enter second number: "))
        result = calculate(num1, num2, op)
        print(f"Result: {result}")
        
    except ValueError:
        print("Error: Please enter valid numbers")
    except KeyboardInterrupt:
        break

print("Calculator closed.")
```

That's it. Simple function that does the math, simple loop that gets input and displays results. No classes, no complex error handling, just the core functionality that works.