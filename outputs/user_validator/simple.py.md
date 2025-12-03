# User Validator - Simple

**Prompt:** Write code to validate user registration data: email must be valid format, password must be at least 8 characters with a number, username must be alphanumeric.

**Output tokens:** 307

## Response

```python
import re

def validate_registration(email, password, username):
    errors = []
    
    # Validate email
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        errors.append("Invalid email format")
    
    # Validate password
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    # Validate username
    if not username.isalnum():
        errors.append("Username must be alphanumeric")
    
    return len(errors) == 0, errors

# Usage example:
if __name__ == "__main__":
    valid, errors = validate_registration("user@example.com", "password123", "user123")
    if valid:
        print("Registration data is valid")
    else:
        print("Validation errors:")
        for error in errors:
            print(f"- {error}")
```

That's it. One function that takes the three inputs, checks each requirement, and returns whether it's valid plus any error messages. No classes, no complex abstractions - just the validation logic you need.