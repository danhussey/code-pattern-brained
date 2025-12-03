# Fibonacci - Simple

**Prompt:** Write a function that returns the nth Fibonacci number.

**Output tokens:** 125

## Response

```python
def fibonacci(n):
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b
```

This is the most straightforward iterative solution. It handles the base cases (0 and 1) and uses two variables to track the previous two numbers, avoiding recursion overhead and keeping it simple with O(n) time and O(1) space complexity.