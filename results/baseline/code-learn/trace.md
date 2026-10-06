### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/', '/workspace/tests/']

### Tool call: ls
{"path": "workspace/inventory"}

### Tool call: ls
{"path": "workspace/tests"}

### Tool call: read_file
{"file_path": "workspace/README.md"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py']

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_report.py']

### Tool result
@@ lines 1-5 of 5 @@
# inventory

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 0.3.1
- initial import

### Tool call: read_file
{"file_path": "workspace/inventory/__init__.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py"}

### Tool call: read_file
{"file_path": "workspace/tests/test_report.py"}

### Tool result
@@ lines 1-1 @@
System reminder: File exists but has empty contents

### Tool result
@@ lines 1-12 of 12 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'

### Tool result
@@ lines 1-25 of 25 @@
"""Price utilities for the inventory package."""
from decimal import Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "")
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"))

### Tool result
@@ lines 1-25 of 25 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return [item["name"] for item in items if item["qty"] <= threshold]

### Tool result
@@ lines 1-32 of 32 @@
from decimal import Decimal

from inventory.export import to_csv_row
from inventory.pricing import apply_discount
from inventory.report import low_stock, total_value


def test_total_value_plain():
    items = [{"name": "pen", "price": "$2.50", "qty": 4}]
    assert total_value(items) == Decimal("10.00")


def test_total_value_thousands_separator():
    items = [{"name": "laptop", "price": "$1,299.50", "qty": 2}]
    assert total_value(items) == Decimal("2599.00")


def test_discount_rounding_half_up():
    assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")


def test_total_value_with_discount():
    items = [{"name": "desk", "price": "100.00", "qty": 1, "discount": 15}]
    assert total_value(items) == Decimal("85.00")


def test_low_stock_basic():
    assert low_stock([{"name": "pen", "qty": 2}, {"name": "ink", "qty": 9}]) == ["pen"]


def test_csv_row_plain_name():
    assert to_csv_row({"name": "pen", "price": "2.5", "qty": 4}) == "pen,2.50,4"

### Tool call: execute
{"command": "cd workspace && ls -la && python -m pytest tests -q 2>&1 | tail -40"}

### Tool call: glob
{"pattern": "**/*"}

### Tool result
total 10
drwxr-xr-x 1 toang 197609   0 Oct  6 16:08 .
drwxr-xr-x 1 toang 197609   0 Oct  6 16:47 ..
-rw-r--r-- 1 toang 197609  60 Oct  6 16:08 CHANGELOG.md
-rw-r--r-- 1 toang 197609 124 Oct  6 16:08 README.md
drwxr-xr-x 1 toang 197609   0 Oct  6 16:32 inventory
drwxr-xr-x 1 toang 197609   0 Oct  6 16:32 tests
    self.pluginmanager.load_setuptools_entrypoints("pytest11")
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\pluggy\_manager.py", line 416, in load_setuptools_entrypoints
    plugin = ep.load()
             ^^^^^^^^^
  File "~\AppData\Local\Programs\Python\Python312\Lib\importlib\metadata\__init__.py", line 205, in load
    module = import_module(match.group('module'))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "~\AppData\Local\Programs\Python\Python312\Lib\importlib\__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\_pytest\assertion\rewrite.py", line 188, in exec_module
    

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/__init__.py', '/workspace/inventory/__pycache__/__init__.cpython-312.pyc', '/workspace/inventory/__pycache__/export.cpython-312.pyc', '/workspace/inventory/__pycache__/pricing.cpython-312.pyc', '/workspace/inventory/__pycache__/report.cpython-312.pyc', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py', '/workspace/tests/__pycache__/test_report.cpython-312-pytest-9.1.1.pyc', '/workspace/tests/test_report.py']

### Tool call: execute
{"command": "cd workspace && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests -q 2>&1 | tail -40"}

### Tool result
<no output>

Exit code: 255
[Command failed with exit code 255]

### Tool call: execute
{"command": "cd workspace && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests -q; echo \"EXIT=$?\""}

### Tool result
[stderr] 'PYTEST_DISABLE_PLUGIN_AUTOLOAD' is not recognized as an internal or external command,
[stderr] operable program or batch file.

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest tests -q 2>&1 | tail -30"}

### Tool result

    def parse_price(text):
        """Convert a price string to a Decimal.
    
        Supported formats:
          "$1,299.50" -> Decimal("1299.50")
          "  12 "     -> Decimal("12")
          "1299.5"    -> Decimal("1299.5")
          "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
        """
        cleaned = text.strip().replace("$", "")
>       return Decimal(cleaned)
               ^^^^^^^^^^^^^^^^
E       decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]

inventory\pricing.py:15: InvalidOperation
_______________________ test_discount_rounding_half_up ________________________

    def test_discount_rounding_half_up():
>       assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")
E       AssertionError: assert Decimal('9.04') == Decimal('9.05')
E        +  where Decimal('9.04') = apply_discount(Decimal('10.05'), 10)
E        +    where Decimal('10.05') = Decimal('10.05')
E        +  and   Decimal('9.05') = Decimal('9.05')

D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\tasks\code-learn\workspace\tests\test_report.py:19: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_report.py::test_total_value_thousands_separator - decimal.I...
FAILED tests/test_report.py::test_discount_rounding_half_up - AssertionError:...
2 failed, 4 passed in 0.06s

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd / && ls -la; echo \"---\"; ls -la /workspace 2>/dev/null; echo \"--- home ---\"; ls -la ~ 2>/dev/null"}

### Tool call: glob
{"pattern": "**/*.md"}

### Tool call: glob
{"pattern": "**/{.editorconfig,.flake8,setup.cfg,pyproject.toml,tox.ini,.pre-commit-config.yaml,AGENTS.md,CONTRIBUTING.md,conventions*}"}

### Tool result
[stderr] The system cannot find the path specified.

Exit code: 1
[Command failed with exit code 1]

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md']

### Tool result
No files found

### Tool call: execute
{"command": "pwd && ls -la && cd .. && pwd && ls -la"}

### Tool result
/c/Users/toang/AppData/Local/Temp/tmp_f7ips4d
total 2724
drwxr-xr-x 1 toang 197609 0 Oct  6 16:47 .
drwxr-xr-x 1 toang 197609 0 Oct  6 16:47 ..
drwxr-xr-x 1 toang 197609 0 Oct  6 16:47 workspace
/c/Users/toang/AppData/Local/Temp
total 381402
drwxr-xr-x 1 toang 197609        0 Oct  6 16:47 .
drwxr-xr-x 1 toang 197609        0 Oct  5 11:37 ..
-rw-r--r-- 1 toang 197609       53 Oct  6 14:11 .ses
-rw-r--r-- 1 toang 197609     8404 Oct  3 23:05 005aa716-cfab-473c-9e53-e5841f15c060.tmp.mp3
-rw-r--r-- 1 toang 197609  6452424 Oct  6 16:40 009fd2df-cfba-46c0-86ac-1d79df975ad9.tmp
-rw-r--r-- 1 toang 197609   605218 Oct  3 23:05 00f7856e-2cfd-4e74-9dda-877b98f962b7.tmp.css
-rw-r--r-- 1 toang 197609   304886 Oct  5 15:38 01935d48-6d6e-4109-bd52-1d85f41ee3d8.tmp.ico
-rw-r--r-- 1 toang 197609   304886 Oct  5 15:38 02869800-1131-4e1c-af5d-3f5bc9dbc83b.tmp.ico
-rw-r--r-- 1 toang 197609  2453082 Oct  4 10:53 028b833a-6603-4066-9e45-cd439729f75e.tmp.webm
-rw-r--r-- 1 toang 197609    11203 Oct  6 16:08 03b5b632-771b-4a01-8ad1-8e2ba91da4c5.tmp
-rw-r--r-- 1 toang 197609 10824649 Oct  4 10:53 03d86975-8d47-456b-98c2-07d846364aad.tmp.js
-rw-r--r-- 1 toang 197609   304886 Oct  5 15:38 03dc1889-b70d-4188-8dcf-15cf677cbc28.tmp.ico
-rw-r--r-- 1 toang 197609   605218 Oct  6 10:08 05203dfd-5312-4e84-b2e3-584aafc7a4bf.tmp.css
-rw-r--r-- 1 toang 197609    29508 Sep 29 19:57 05590b38-089a-439e-abff-8b764b8c7b26.png
-rw-r--r-- 1 toang 197609   304886 Sep 29 21:48 073102aa-63e3-4600-a8d1-63e6bd39dfa4.tmp.ico


### Tool call: execute
{"command": "ls -la /d/VIN_AI/lab_day_20/ 2>/dev/null; echo \"===\"; ls -d /d/VIN_AI 2>/dev/null; echo \"exit $?\""}

### Tool result
[stderr] The system cannot find the path specified.

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "cd workspace && python -m black --version 2>&1; python -m ruff --version 2>&1; python -m flake8 --version 2>&1; python -m pyflakes --version 2>&1"}

### Tool result
D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Scripts\python.exe: No module named black

Exit code: 1
[Command failed with exit code 1]

### Assistant
Now I understand the failures. Let me look at the spec details and fix each function. Let me apply the fixes:

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "\"\"\"Price utilities for the inventory package.\"\"\"\nfrom decimal import Decimal\n\n\ndef parse_price(text):\n    \"\"\"Convert a price string to a Decimal.\n\n    Supported formats:\n      \"$1,299.50\" -> Decimal(\"1299.50\")\n      \"  12 \"     -> Decimal(\"12\")\n      \"1299.5\"    -> Decimal(\"1299.5\")\n      \"(12.00)\"   -> Decimal(\"-12.00\")   # accounting style: parentheses mean negative\n    \"\"\"\n    cleaned = text.strip().replace(\"$\", \"\")\n    return Decimal(cleaned)\n\n\ndef apply_discount(price, percent):\n    \"\"\"Return `price` after a percentage discount.\n\n    The result is a Decimal rounded to 2 decimal places using the\n    commercial rule \"round half up\" (0.005 -> 0.01).\n    \"\"\"\n    discounted = price * (100 - percent) / 100\n    return discounted.quantize(Decimal(\"0.01\"))", "new_string": "\"\"\"Price utilities for the inventory package.\"\"\"\nfrom decimal import ROUND_HALF_UP, Decimal\n\n\ndef parse_price(text):\n    \"\"\"Convert a price string to a Decimal.\n\n    Supported formats:\n      \"$1,299.50\" -> Decimal(\"1299.50\")\n      \"  12 \"     -> Decimal(\"12\")\n      \"1299.5\"    -> Decimal(\"1299.5\")\n      \"(12.00)\"   -> Decimal(\"-12.00\")   # accounting style: parentheses mean negative\n    \"\"\"\n    cleaned = text.strip().replace(\"$\", \"\").replace(\",\", \"\")\n    if cleaned.startswith(\"(\") and cleaned.endswith(\")\"):\n        return -Decimal

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Tool call: edit_file
{"file_path": "workspace/inventory/export.py", "new_string": "    price = parse_price(item[\"price\"])\n    name = item[\"name\"]\n    if \",\" in name or '\"' in name:\n        name = '\"' + name.replace('\"', '\"\"') + '\"'\n    return f\"{name},{price:.2f},{item['qty']}\"", "old_string": "    price = parse_price(item[\"price\"])\n    return f'{item[\"name\"]},{price:.2f},{item[\"qty\"]}'"}

### Tool call: edit_file
{"file_path": "workspace/inventory/report.py", "new_string": "def low_stock(items, threshold=5):\n    \"\"\"Names of the items whose quantity is strictly below `threshold`.\n\n    The names are sorted alphabetically, ignoring case.\n    \"\"\"\n    names = [item[\"name\"] for item in items if item[\"qty\"] < threshold]\n    return sorted(names, key=str.lower)", "old_string": "def low_stock(items, threshold=5):\n    \"\"\"Names of the items whose quantity is strictly below `threshold`.\n\n    The names are sorted alphabetically, ignoring case.\n    \"\"\"\n    return [item[\"name\"] for item in items if item[\"qty\"] <= threshold]"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/export.py'

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/report.py'

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q -p no:cacheprovider 2>&1 | tail -15"}

### Tool call: execute
{"command": "cd workspace && python -c \"\nfrom decimal import Decimal\nfrom inventory.pricing import parse_price, apply_discount\nfrom inventory.report import low_stock, total_value\nfrom inventory.export import to_csv_row\nprint(parse_price('\\$1,299.50'))\nprint(parse_price('  12 '))\nprint(parse_price('1299.5'))\nprint(parse_price('(12.00)'))\nprint(apply_discount(Decimal('10.05'), 10))\nprint(low_stock([{'name':'Pen','qty':2},{'name':'ink','qty':5},{'name':'Apple','qty':1}], 5))\nprint(to_csv_row({'name':'a,b','price':'2.5','qty':4}))\nprint(to_csv_row({'name':'a\\\"b','price':'2.5','qty':4}))\nprint(to_csv_row({'name':'pen','price':'2.5','qty':4}))\n\""}

### Tool result
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\_pytest\assertion\rewrite.py", line 188, in exec_module
    exec(co, module.__dict__)
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 4, in <module>
    import asyncio
  File "~\AppData\Local\Programs\Python\Python312\Lib\asyncio\__init__.py", line 43, in <module>
    from .windows_events import *
  File "~\AppData\Local\Programs\Python\Python312\Lib\asyncio\windows_events.py", line 8, in <module>
    import _overlapped
OSError: [WinError 10106] The requested service provider could not be loaded or initialized

[Command succeeded with exit code 0]

### Tool result
<no output>
[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1&& python -m pytest tests -q 2>&1 | tail -15"}

### Tool result
......                                                                   [100%]
6 passed in 0.04s

[Command succeeded with exit code 0]

### Tool call: write_file
{"file_path": "/workspace/_check_tmp.py", "content": "from decimal import Decimal\n\nfrom inventory.export import to_csv_row\nfrom inventory.pricing import apply_discount, parse_price\nfrom inventory.report import low_stock, total_value\n\nassert parse_price(\"$1,299.50\") == Decimal(\"1299.50\")\nassert parse_price(\"  12 \") == Decimal(\"12\")\nassert parse_price(\"1299.5\") == Decimal(\"1299.5\")\nassert parse_price(\"(12.00)\") == Decimal(\"-12.00\")\nassert str(parse_price(\"(12.00)\")) == \"-12.00\"\n\nassert apply_discount(Decimal(\"10.05\"), 10) == Decimal(\"9.05\")\nassert apply_discount(Decimal(\"10.04\"), 10) == Decimal(\"9.04\")   # 9.036 -> 9.04\nassert apply_discount(Decimal(\"10.00\"), 0) == Decimal(\"10.00\")\n\nassert low_stock([{\"name\": \"Pen\", \"qty\": 2}, {\"name\": \"ink\", \"qty\": 5},\n                  {\"name\": \"apple\", \"qty\": 1}], 5) == [\"apple\", \"Pen\"]\nassert low_stock([{\"name\": \"a\", \"qty\": 5}]) == []  # strictly below\n\nassert to_csv_row({\"name\": \"pen\", \"price\": \"2.5\", \"qty\": 4}) == \"pen,2.50,4\"\nassert to_csv_row({\"name\": \"a,b\", \"price\": \"2.5\", \"qty\": 4}) == '\"a,b\",2.50,4'\nassert to_csv_row({\"name\": 'a\"b', \"price\": \"2.5\", \"qty\": 4}) == '\"a\"\"b\",2.50,4'\n\nassert total_value([{\"name\": \"pen\", \"price\": \"$2.50\", \"qty\": 4}]) == Decimal(\"10.00\")\nprint(\"ALL OK\")\n"}

### Tool result
Updated file /workspace/_check_tmp.py

### Tool call: execute
{"command": "cd workspace && python _check_tmp.py"}

### Tool result
ALL OK

[Command succeeded with exit code 0]

### Tool call: delete
{"file_path": "/workspace/_check_tmp.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/export.py"}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py"}

### Tool result
Deleted /workspace/_check_tmp.py

### Tool result
@@ lines 1-27 of 27 @@
"""Price utilities for the inventory package."""
from decimal import ROUND_HALF_UP, Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "").replace(",", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        return -Decimal(cleaned[1:-1])
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

### Tool result
@@ lines 1-15 of 15 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    name = item["name"]
    if "," in name or '"' in name:
        name = '"' + name.replace('"', '""') + '"'
    return f"{name},{price:.2f},{item['qty']}"

### Tool result
@@ lines 1-26 of 26 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    names = [item["name"] for item in items if item["qty"] < threshold]
    return sorted(names, key=str.lower)

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1&& python -m pytest tests -q 2>&1 | tail -5"}

### Tool result
......                                                                   [100%]
6 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
All tests pass and the behavior now matches the docstrings.

## Summary

The failing tests were caused by three source functions not honoring their docstrings. I fixed the code (tests untouched):

**`inventory/pricing.py`**
- `parse_price`: now strips the `$`, removes thousands separators (`,`) as the docstring specifies (`"$1,299.50"` → `Decimal("1299.50")`), and handles accounting-style parentheses (`"(12.00)"` → `Decimal("-12.00")`).
- `apply_discount`: now quantizes with `ROUND_HALF_UP` instead of the default `ROUND_HALF_EVEN`, so `0.005` rounds up (`10.05` with a 10% discount → `9.05`, not `9.04`).

**`inventory/report.py`**
- `low_stock`: changed the comparison from `<=` to `<` (quantity *strictly* below the threshold) and now sorts the returned names alphabetically, case-insensitively.

**`inventory/export.py`**
- `to_csv_row`: now implements RFC 4180 quoting — a name containing a comma or a double quote is wrapped in double quotes with internal quotes doubled.

I verified the full suite (`6 passed`) plus extra edge cases against the docstring spec: thousands separators, accounting negatives, half-up rounding, strict-below/low-case sorting, and CSV quoting for both commas and quotes.