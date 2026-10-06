"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use proactively when starting a task to explore files, inspect directory layout, "
                "read docstrings, README, logs, or data samples. Reports facts without modifying files."
            ),
            "system_prompt": (
                "You are an exploratory research subagent. Your role is to examine the repository, "
                "inspect file layouts, read docstrings, README, logs, or data files, and report key facts, "
                "constraints, and requirements accurately to the main agent. You must never modify or delete any files."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when specific code, script, or data changes need to be written or executed. "
                "Applies edits, runs pytest or python scripts, and reports the results."
            ),
            "system_prompt": (
                "You are an implementation subagent. Your role is to perform changes to workspace files, "
                "write code or clean data according to instructions, run tests or scripts via the shell, "
                "and report the execution outcomes and any errors back to the main agent."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use after implementation or before declaring completion to perform independent quality checks, "
                "verify test results, check against edge cases, formatting rules, or docstrings. Do not edit files."
            ),
            "system_prompt": (
                "You are a quality assurance and code review subagent. Your role is to independently review workspace changes, "
                "check edge cases, verify that requirements and conventions are strictly met, run tests if needed, "
                "and report any discrepancies or bugs to the main agent without modifying any files."
            ),
        },
    ]
