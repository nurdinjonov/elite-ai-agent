"""Terminal command execution tool with safety guardrails."""

import subprocess

from langchain_core.tools import tool

_BLOCKED_PATTERNS: list[str] = [
    "rm -rf /",
    "mkfs",
    "dd if=",
    ":(){ :|:& };:",
    "shutdown",
    "reboot",
]

_TIMEOUT_SECONDS = 60


@tool
def run_terminal_command_tool(command: str) -> str:
    """Execute a shell command and return its output.

    Dangerous commands are blocked before execution.  The command times out
    after 60 seconds.

    Args:
        command: The shell command string to execute.

    Returns:
        Combined stdout/stderr output, or an error/block message.
    """
    # Safety check
    for pattern in _BLOCKED_PATTERNS:
        if pattern in command:
            return f"🚫 Xavfli buyruq bloklandi: '{pattern}' topildi."

    try:
        # shell=True is intentional here — this tool is designed to execute
        # arbitrary shell commands as directed by the agent.  The blocked-
        # pattern list above mitigates the most dangerous operations.
        result = subprocess.run(  # noqa: S602
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=_TIMEOUT_SECONDS,
        )
        parts: list[str] = []
        if result.stdout:
            parts.append(f"**stdout:**\n{result.stdout}")
        if result.stderr:
            parts.append(f"**stderr:**\n{result.stderr}")
        parts.append(f"**Exit kodi:** {result.returncode}")
        return "\n\n".join(parts) if parts else "Buyruq bajarildi. Hech qanday chiqish yo'q."

    except subprocess.TimeoutExpired:
        return f"⏱ Buyruq {_TIMEOUT_SECONDS} soniya ichida tugamadi va to'xtatildi."
    except Exception as exc:  # noqa: BLE001
        return f"Terminal xatosi: {exc}"
