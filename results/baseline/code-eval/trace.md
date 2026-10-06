### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant
I'll start by exploring the workspace structure.

### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: ls
{"path": "workspace/bookings"}

### Tool call: ls
{"path": "workspace/tests"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "workspace/README.md"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py"}

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: execute
{"command": "cd workspace && ls -la && python -m pytest tests -q 2>&1 | tail -30"}

### Tool call: glob
{"pattern": "**/*", "path": "workspace"}

### Tool result
total 6
drwxr-xr-x 1 toang 197609   0 Oct  6 16:08 .
drwxr-xr-x 1 toang 197609   0 Oct  6 17:05 ..
-rw-r--r-- 1 toang 197609  60 Oct  6 16:08 CHANGELOG.md
-rw-r--r-- 1 toang 197609 123 Oct  6 16:08 README.md
drwxr-xr-x 1 toang 197609   0 Oct  6 16:32 bookings
drwxr-xr-x 1 toang 197609   0 Oct  6 16:32 tests
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\_pytest\assertion\rewrite.py", line 188, in exec_module
    exec(co, module.__dict__)
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\anyio\pytest_plugin.py", line 305, in <module>
    @pytest.fixture(scope="module", params=get_available_backends())
                                           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\anyio\_core\_eventloop.py", line 153, in get_available_backends
    get_async_backend(backend_name)
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\anyio\_core\_eventloop.py", line 206, in get_async_backend
 

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-312.pyc', '/workspace/bookings/__pycache__/billing.cpython-312.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-312.pyc', '/workspace/bookings/__pycache__/schedule.cpython-312.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-312.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-312-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q -p no:anyio 2>&1 | tail -20"}

### Tool result
    from ._utils import (
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\_pytest\assertion\rewrite.py", line 188, in exec_module
    exec(co, module.__dict__)
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\langsmith\_openapi_client\_utils\__init__.py", line 2, in <module>
    from ._sync import asyncify as asyncify
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\_pytest\assertion\rewrite.py", line 188, in exec_module
    exec(co, module.__dict__)
  File "D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Lib\site-packages\langsmith\_openapi_client\_utils\_sync.py", line 3, in <module>
    import asyncio
  File "~\AppData\Local\Programs\Python\Python312\Lib\asyncio\__init__.py", line 43, in <module>
    from .windows_events import *
  File "~\AppData\Local\Programs\Python\Python312\Lib\asyncio\windo

### Tool call: execute
{"command": "cd workspace && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests -q 2>&1 | tail -20"}

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
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1&& python -m pytest tests -q & echo EXIT=%ERRORLEVEL%"}

### Tool result
FF.                                                                      [100%]
================================== FAILURES ===================================
______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\tasks\code-eval\workspace\tests\test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
bookings\schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
bookings\schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare number means minutes
        Surrounding whitespace is ignored.
        """
        m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
        if not m:
>           raise ValueError(f"bad duration: {text!r}")
E           ValueError: bad duration: '2h'

bookings\timeutil.py:18:

### Tool call: execute
{"command": "cd .. && ls -a; echo \"---\"; ls -a tasks 2>nul; echo \"---\"; ls -a .. 2>nul"}

### Tool result
<no output>

Exit code: 2
[Command failed with exit code 2]

### Tool call: ls
{"path": "."}

### Tool result
['/workspace/']

### Assistant
Now let me apply the fixes.

### Tool call: edit_file
{"file_path": "workspace/bookings/billing.py", "old_string": "    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    return round(minutes / block)", "new_string": "    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(f\"minutes must be >= 0: {minutes!r}\")\n    # Integer ceiling division: exact, so no float rounding surprises.\n    return -(-minutes // block)"}

### Tool call: edit_file
{"file_path": "workspace/bookings/schedule.py", "old_string": "def add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots", "new_string": "def add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    new_slots = list(slots) if slots is not None else []\n    new_slots.append(slot)\n    return new_slots"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Tool call: edit_file
{"file_path": "workspace/bookings/timeutil.py", "new_string": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n_DURATION_RE = re.compile(\n    r\"(?P<hours>\\d+)h(?:(?P<hour_minutes>\\d+)m)?\"  # \"1h30m\", \"2h\"\n    r\"|(?P<minutes>\\d+)m\"  # \"45m\"\n    r\"|(?P<clock_hours>\\d+):(?P<clock_minutes>\\d+)\"  # \"1:30\"\n    r\"|(?P<bare>\\d+)\"  # \"45\" (minutes)\n)\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    match = _DURATION_RE.fullmatch(text.strip())\n    if not match:\n        raise ValueError(f\"bad duration: {text!r}\")\n\n    if match.group(\"hours\") is not None:\n        return int(match.group(\"hours\")) * 60 + int(match.group(\"hour_minutes\") or 0)\n    if match.group(\"clock_hours\") is not None:\n        return int(match.group(\"clock_hours\")) * 60 + int(match.group(\"clock_minutes\"))\n    if match.group(\"minutes\") is not None:\n        return int(match.group(\"minutes\"))\n    return int(match.group(\"bare\"))\n", "old_string": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"4

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1&& python -m pytest tests -q & echo EXIT=%ERRORLEVEL%"}

### Tool result
...                                                                      [100%]
3 passed in 0.04s
EXIT=0

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -m ruff --version 2>&1 | head -2; python -m black --version 2>&1 | head -2; python -m flake8 --version 2>&1 | head -2"}

### Tool result
head: invalid trailing option -- ;
Try 'head --help' for more information.

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -m ruff --version & python -m black --version & python -m flake8 --version"}

### Tool result
[stderr] D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Scripts\python.exe: No module named ruff
[stderr] D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Scripts\python.exe: No module named black
[stderr] D:\VIN_AI\lab_day_20\K4-L3L4-Track3-Day20-LuongKhanhToan-2A202602836-AdvanceMultiAgents\.venv\Scripts\python.exe: No module named flake8

Exit code: 1
[Command failed with exit code 1]

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool result
@@ lines 1-33 of 33 @@
"""Time helpers for the bookings package."""
import re

_DURATION_RE = re.compile(
    r"(?P<hours>\d+)h(?:(?P<hour_minutes>\d+)m)?"  # "1h30m", "2h"
    r"|(?P<minutes>\d+)m"  # "45m"
    r"|(?P<clock_hours>\d+):(?P<clock_minutes>\d+)"  # "1:30"
    r"|(?P<bare>\d+)"  # "45" (minutes)
)


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    match = _DURATION_RE.fullmatch(text.strip())
    if not match:
        raise ValueError(f"bad duration: {text!r}")

    if match.group("hours") is not None:
        return int(match.group("hours")) * 60 + int(match.group("hour_minutes") or 0)
    if match.group("clock_hours") is not None:
        return int(match.group("clock_hours")) * 60 + int(match.group("clock_minutes"))
    if match.group("minutes") is not None:
        return int(match.group("minutes"))
    return int(match.group("bare"))

### Tool call: edit_file
{"file_path": "workspace/bookings/timeutil.py", "old_string": "    if match.group(\"hours\") is not None:\n        return int(match.group(\"hours\")) * 60 + int(match.group(\"hour_minutes\") or 0)\n    if match.group(\"clock_hours\") is not None:\n        return int(match.group(\"clock_hours\")) * 60 + int(match.group(\"clock_minutes\"))\n    if match.group(\"minutes\") is not None:\n        return int(match.group(\"minutes\"))\n    return int(match.group(\"bare\"))", "new_string": "    hours = match.group(\"hours\")\n    if hours is not None:\n        extra_minutes = match.group(\"hour_minutes\") or 0\n        return int(hours) * 60 + int(extra_minutes)\n\n    clock_hours = match.group(\"clock_hours\")\n    if clock_hours is not None:\n        clock_minutes = match.group(\"clock_minutes\")\n        return int(clock_hours) * 60 + int(clock_minutes)\n\n    if match.group(\"minutes\") is not None:\n        return int(match.group(\"minutes\"))\n\n    return int(match.group(\"bare\"))"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: write_file
{"file_path": "workspace/_check.py", "content": "from bookings.billing import billable_blocks\nfrom bookings.calendar_export import slot_end\nfrom bookings.schedule import add_slot, total_minutes\nfrom bookings.timeutil import parse_duration\n\nassert parse_duration(\"1h30m\") == 90\nassert parse_duration(\"2h\") == 120\nassert parse_duration(\"45m\") == 45\nassert parse_duration(\"1:30\") == 90\nassert parse_duration(\"45\") == 45\nassert parse_duration(\"  1h30m  \") == 90\nassert parse_duration(\"0\") == 0\nassert parse_duration(\"0h0m\") == 0\nassert isinstance(parse_duration(\"2h\"), int)\nfor bad in (\"\", \"abc\", \"1h30\", \"h\", \"1.5h\", \"1:30pm\", \"-5\", \"1h30s\"):\n    try:\n        parse_duration(bad)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError(f\"expected ValueError for {bad!r}\")\n\nassert total_minutes([\"1h30m\", \"2h\"]) == 210\nassert total_minutes([\"1h30m\", \"2h\", \"45\"]) == 255\nassert total_minutes([]) == 0\nassert total_minutes((\"45m\",)) == 45\n\nassert billable_blocks(0) == 0\nassert billable_blocks(1) == 1\nassert billable_blocks(15) == 1\nassert billable_blocks(16) == 2\nassert billable_blocks(20) == 2\nassert billable_blocks(45) == 3\nassert billable_blocks(30, 30) == 1\nassert billable_blocks(31, 30) == 2\nassert billable_blocks(10**15 + 1, 15) == -(-(10**15 + 1) // 15)\ntry:\n    billable_blocks(-1)\nexcept ValueError:\n    pass\nelse:\n    raise AssertionError(\"expected ValueError for negative minutes\

### Tool result
Updated file /workspace/_check.py

### Tool call: execute
{"command": "cd workspace && python _check.py & echo EXIT=%ERRORLEVEL%"}

### Tool result
all docstring checks passed
EXIT=0

[Command succeeded with exit code 0]

### Tool call: delete
{"file_path": "workspace/_check.py"}

### Tool call: edit_file
{"file_path": "workspace/CHANGELOG.md", "old_string": "## Unreleased\n", "new_string": "## Unreleased\n- Fix `billable_blocks` to round up (and reject negative minutes)\n- Fix `parse_duration` to accept all documented formats (\"2h\", \"45m\", \"1:30\", \"45\")\n- Fix `add_slot` to return a new list instead of using a shared mutable default\n"}

### Tool result
Deleted /workspace/_check.py

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1&& python -m pytest tests -q & echo EXIT=%ERRORLEVEL% & del /s /q bookings\\__pycache__ tests\\__pycache__ >nul 2>&1 & ls"}

### Tool result
...                                                                      [100%]
3 passed in 0.01s
EXIT=0 
CHANGELOG.md
README.md
bookings
tests

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool result
@@ lines 1-40 of 40 @@
"""Time helpers for the bookings package."""
import re

_DURATION_RE = re.compile(
    r"(?P<hours>\d+)h(?:(?P<hour_minutes>\d+)m)?"  # "1h30m", "2h"
    r"|(?P<minutes>\d+)m"  # "45m"
    r"|(?P<clock_hours>\d+):(?P<clock_minutes>\d+)"  # "1:30"
    r"|(?P<bare>\d+)"  # "45" (minutes)
)


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    match = _DURATION_RE.fullmatch(text.strip())
    if not match:
        raise ValueError(f"bad duration: {text!r}")

    hours = match.group("hours")
    if hours is not None:
        extra_minutes = match.group("hour_minutes") or 0
        return int(hours) * 60 + int(extra_minutes)

    clock_hours = match.group("clock_hours")
    if clock_hours is not None:
        clock_minutes = match.group("clock_minutes")
        return int(clock_hours) * 60 + int(clock_minutes)

    if match.group("minutes") is not None:
        return int(match.group("minutes"))

    return int(match.group("bare"))

### Tool result
@@ lines 1-14 of 14 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    if minutes < 0:
        raise ValueError(f"minutes must be >= 0: {minutes!r}")
    # Integer ceiling division: exact, so no float rounding surprises.
    return -(-minutes // block)

### Tool result
@@ lines 1-18 of 18 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=None):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    new_slots = list(slots) if slots is not None else []
    new_slots.append(slot)
    return new_slots

### Assistant
Done. The suite passes (`3 passed`) and each function now matches its docstring.

## Changes

**`bookings/timeutil.py` — `parse_duration`** (root cause of the `total_minutes` failure)
- The regex only matched `"1h30m"`, so `"2h"`, `"45m"`, `"1:30"` and bare `"45"` raised `ValueError`. Replaced it with a single named-group pattern compiled once at module level (`_DURATION_RE`) covering all five documented formats, still ignoring surrounding whitespace and still raising `ValueError` for anything else.

**`bookings/billing.py` — `billable_blocks`**
- Used `round()`, so 20 min → 1 block instead of rounding up. Switched to exact integer ceiling division `-(-minutes // block)` (avoids float rounding for large values) and added the documented `ValueError` for negative `minutes`.

**`bookings/schedule.py` — `add_slot`**
- Had a mutable default argument (`slots=[]`) and mutated/returned the caller's list, so calls shared state and the input was modified. Now defaults to `None`, copies the input into a fresh list, appends, and returns it — callers' lists are never mutated and separate calls don't leak state.

**`bookings/CHANGELOG.md`** — recorded the three fixes under `## Unreleased`.

I did not touch `tests/`, `calendar_export.py` (`slot_end` was already correct), or `README.md`. I also removed the throwaway verification script and `__pycache__` artifacts, so the only files changed are the three modules plus the changelog. Note the sandbox's `pytest` needs `PYTEST_DISABLE_PLUGIN_AUTO