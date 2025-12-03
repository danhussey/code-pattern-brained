# File Processor - Simple

**Prompt:** Write code that reads a CSV file and outputs JSON with the same data.

**Output tokens:** 153

## Response

```python
import csv
import json

def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)

# Usage
csv_to_json('input.csv', 'output.json')
```

That's it. This reads a CSV file and writes the exact same data as JSON. Each CSV row becomes a JSON object, and the column headers become the object keys.