# UI Collector Tests

This directory contains Robot Framework tests for comparing different UI element collection strategies.

## Available Collectors

- **js_query**: JavaScript querySelector-based approach (original/default)
- **axtree**: Accessibility Tree-based approach

## Test Files

### test_js_query.robot
Tests the JSQuery collector in isolation on various websites.

```bash
robot tests/atest/collectors/test_js_query.robot
```

### test_axtree.robot
Tests the AXTree collector in isolation on various websites.

```bash
robot tests/atest/collectors/test_axtree.robot
```

### compare_all.robot
Compares both collectors side-by-side on the same pages to analyze differences.

```bash
robot tests/atest/collectors/compare_all.robot
```

## Test Sites

The tests use the following websites:
- **https://the-internet.herokuapp.com/login** - Simple login form
- **https://www.saucedemo.com** - Demo e-commerce login
- **https://react-shopping-cart-67954.firebaseapp.com/** - React SPA

## Running Tests

### Run all collector tests
```bash
robot tests/atest/collectors/
```

### Run with specific tags
```bash
# Only JSQuery tests
robot --include js_query tests/atest/collectors/

# Only AXTree tests
robot --include axtree tests/atest/collectors/

# Only comparison tests
robot --include compare tests/atest/collectors/

# Only login form tests
robot --include login tests/atest/collectors/
```

## Expected Output

The tests will log:
- Number of elements found by each collector
- Sample elements with their attributes
- Comparison statistics (differences, element type counts)
- Detailed element dictionaries for debugging

## Adding New Collectors

To add a new collector strategy:

1. Create a new class in `Agent/platforms/collectors/` that inherits from `BaseUICollector`
2. Register it in `collector_factory.py`
3. Create a new test file `test_<name>.robot`
4. Update `compare_all.robot` to include the new collector

Example:
```python
# Agent/platforms/collectors/my_new_collector.py
from Agent.platforms.collectors.base_collector import BaseUICollector

class MyNewCollector(BaseUICollector):
    def get_name(self) -> str:
        return "my_new"
    
    def collect_elements(self, max_items: int = 150):
        # Your implementation
        pass

# In collector_factory.py
from Agent.platforms.collectors.my_new_collector import MyNewCollector
CollectorRegistry.register("my_new", MyNewCollector)
```

Then use it:
```robot
Library    Agent.platforms._webconnector.WebConnectorRF    my_new    AS    Connector
```

