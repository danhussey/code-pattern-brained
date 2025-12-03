# Pattern-Brained vs Simple

What happens when you tell an LLM to use design patterns "liberally"?

**11x more code.** For the same problems.

## Results

| Problem | Pattern-Brained | Simple | Ratio |
|---------|----------------|--------|-------|
| Reverse String | 2,023 tokens | 58 tokens | 34.9x |
| Fibonacci | 2,660 tokens | 125 tokens | 21.3x |
| FizzBuzz | 1,839 tokens | 116 tokens | 15.9x |
| File Processor | 3,461 tokens | 153 tokens | 22.6x |
| ... | ... | ... | ... |
| **Total** | **29,344** | **2,581** | **11.37x** |

See [outputs/](outputs/) for the full side-by-side comparisons.

## Highlights

**Reverse a string (simple):**
```python
def reverse_string(s):
    return s[::-1]
```

**Reverse a string (pattern-brained):** A `ReversalStrategy` Protocol, three strategy implementations, a `ReversalStrategyFactory`, a `StringValidator`, a `StringReverser`, and a `StringReversalService` facade. [Full output →](outputs/reverse_string/pattern_brained.py.md)

## Run it yourself

```bash
uv run python compare.py
```

Requires `ANTHROPIC_API_KEY` in your environment. Costs ~$0.50.

## Blog post

[Read the full writeup →](post.md)
