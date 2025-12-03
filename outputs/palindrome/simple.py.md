# Palindrome Checker - Simple

**Prompt:** Write a function that checks if a string is a palindrome.

**Output tokens:** 113

## Response

```python
def is_palindrome(s):
    return s == s[::-1]
```

That's it. Takes a string, compares it to its reverse. Returns `True` if they match, `False` otherwise.

If you need to ignore case and spaces (common palindrome requirement), here's the slightly longer version:

```python
def is_palindrome(s):
    s = s.lower().replace(' ', '')
    return s == s[::-1]
```