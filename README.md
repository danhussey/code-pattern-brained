# Pattern-Brained vs Simple

[![Blog Post](https://img.shields.io/badge/Read%20the-Blog%20Post-blue?style=for-the-badge)](https://danhussey.bearblog.dev/i-made-claude-use-design-patterns-and-it-wrote-11x-more-code/)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Claude](https://img.shields.io/badge/Powered%20by-Claude-orange?style=for-the-badge)](https://anthropic.com)

---

What happens when you tell an LLM to use design patterns "liberally"?

**11x more code.** For the same problems.

## Results

| Problem | Pattern-Brained | Simple | Ratio |
|---------|----------------|--------|-------|
| Reverse String | 2,023 tokens | 58 tokens | **34.9x** |
| Fibonacci | 2,660 tokens | 125 tokens | **21.3x** |
| File Processor | 3,461 tokens | 153 tokens | **22.6x** |
| FizzBuzz | 1,839 tokens | 116 tokens | **15.9x** |
| Rate Limiter | 3,756 tokens | 319 tokens | 11.8x |
| Calculator | 2,993 tokens | 282 tokens | 10.6x |
| Todo List | 3,812 tokens | 397 tokens | 9.6x |
| User Validator | 2,625 tokens | 307 tokens | 8.5x |
| Shopping Cart | 3,717 tokens | 711 tokens | 5.2x |
| Palindrome | 2,458 tokens | 113 tokens | **21.8x** |
| **Total** | **29,344** | **2,581** | **11.37x** |

Browse all outputs in [outputs/](outputs/).

## The Highlight

**Simple:**
```python
def reverse_string(s):
    return s[::-1]
```

**Pattern-brained:** A `ReversalStrategy` Protocol, an enum, three strategy implementations, a `ReversalStrategyFactory`, a `StringValidator`, a `StringReverser`, and a `StringReversalService` facade.

[See the full 230-line version →](outputs/reverse_string/pattern_brained.py.md)

## Run It Yourself

```bash
uv run python compare.py
```

Requires `ANTHROPIC_API_KEY` in your environment. Costs ~$0.50.

## Read More

**[I Made Claude Use Design Patterns and It Wrote 11x More Code →](https://danhussey.bearblog.dev/i-made-claude-use-design-patterns-and-it-wrote-11x-more-code/)**
