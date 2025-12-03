# FizzBuzz - Simple

**Prompt:** Write a function that prints numbers from 1 to 100. For multiples of 3, print 'Fizz'. For multiples of 5, print 'Buzz'. For multiples of both, print 'FizzBuzz'.

**Output tokens:** 116

## Response

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

That's it. Simple, direct, and does exactly what's needed.