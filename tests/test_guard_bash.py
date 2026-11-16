"""Tests for the F20 PreToolUse guard (.claude/hooks/guard_bash.py).

Subset of the human-approved block/allow cases; the hook JSON is fed on stdin.
Exit 2 = blocked, exit 0 = allowed.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

GUARD = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "guard_bash.py"


def run_guard(stdin_text):
    return subprocess.run(
        [sys.executable, "-B", str(GUARD)], input=stdin_text, capture_output=True, text=True, timeout=30
    )


def run_command(command):
    return run_guard(json.dumps({"tool_name": "Bash", "tool_input": {"command": command}}))


@pytest.mark.parametrize(
    "command",
    [
        "rm -rf build",
        "rm -r -f build",
        "rm --recursive --force build",
        "ls && rm -r -f x",
        'bash -c "rm -fr x"',
        "git push origin main --force",
        "git push --force-with-lease",
        "git push origin +main",
        "git reset --hard",
        "git clean -xdf",
        "cat .env",
        "less config/.env.local",
        "tail secrets/token.txt",
        "cat .env.example",
        "echo x > docs/architecture/ARCHITECTURE.md",
        "sed -i 's/a/b/' docs/conventions/CONVENTIONS.md",
        "echo x | tee docs/architecture/ARCHITECTURE.md",
    ],
)
def test_blocked(command):
    result = run_command(command)
    assert result.returncode == 2
    assert "Blocked by .claude/hooks/guard_bash.py" in result.stderr


@pytest.mark.parametrize(
    "command",
    [
        "rm -r build",
        "rm -f file.txt",
        "git push origin TASKS",
        "git reset HEAD~1",
        "git clean -n",
        "cat docs/architecture/ARCHITECTURE.md",
        "docker compose config -q",
        "bash harness/verify.sh --full",
        "python -m pytest tests",
        "ls secrets",  # known F20 gap: secrets dir without a trailing slash is not detected
    ],
)
def test_allowed(command):
    assert run_command(command).returncode == 0


def test_unreadable_input_fails_closed():
    assert run_guard("not json").returncode == 2


def test_missing_command_is_allowed():
    assert run_guard(json.dumps({"tool_input": {}})).returncode == 0
