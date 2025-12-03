# Rate Limiter - Simple

**Prompt:** Write a rate limiter that allows max N requests per minute for a given user ID.

**Output tokens:** 319

## Response

Here's a simple rate limiter using a dictionary to track requests per user:

```python
import time
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, max_requests_per_minute):
        self.max_requests = max_requests_per_minute
        self.user_requests = defaultdict(deque)
    
    def is_allowed(self, user_id):
        now = time.time()
        user_queue = self.user_requests[user_id]
        
        # Remove requests older than 1 minute
        while user_queue and user_queue[0] <= now - 60:
            user_queue.popleft()
        
        # Check if under limit
        if len(user_queue) < self.max_requests:
            user_queue.append(now)
            return True
        
        return False

# Usage
rate_limiter = RateLimiter(max_requests_per_minute=10)

# Check if user can make a request
if rate_limiter.is_allowed("user123"):
    print("Request allowed")
else:
    print("Rate limit exceeded")
```

That's it. Each user gets a deque that stores timestamps of their requests. When checking, we remove old timestamps and see if they're under the limit. Simple and works.