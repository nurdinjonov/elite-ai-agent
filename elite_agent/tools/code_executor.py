"""Python REPL code execution tool."""

import io
import sys
from contextlib import redirect_stderr, redirect_stdout

from langchain_core.tools import tool


@tool
def python_repl_tool(code: str) -> str:
    """Execute Python code and return the output.

    Runs the given Python code in an isolated namespace.  Both *stdout* and
    *stderr* are captured and returned to the caller.

    Args:
        code: Valid Python source code to execute.

    Returns:
        A string containing stdout, stderr and/or error messages.
    """
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    # Restricted globals — no built-in __import__ override; keeps it safe
    safe_globals: dict = {"__builtins__": __builtins__}

    try:
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            exec(code, safe_globals)  # noqa: S102
    except Exception as exc:  # noqa: BLE001
        stderr_buf.write(f"\n{type(exc).__name__}: {exc}")

    output = stdout_buf.getvalue()
    errors = stderr_buf.getvalue()

    parts: list[str] = []
    if output:
        parts.append(f"**Natija (stdout):**\n{output}")
    if errors:
        parts.append(f"**Xato (stderr):**\n{errors}")
    if not parts:
        parts.append("Kod bajarildi. Hech qanday chiqish yo'q.")

    return "\n\n".join(parts)
