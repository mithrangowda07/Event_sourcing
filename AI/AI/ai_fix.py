#!/usr/bin/env python3
"""
AI Fixer Runner (Gemini-only)

Runs `program.py`, captures errors, sends {code + error} to Gemini for
automated fixing, overwrites `program.py` with the returned code, and repeats
until success or max attempts reached.

Usage (from this directory):
  python ai_fix.py --max-attempts 5 --model auto

Environment variables (loaded automatically from .env):
  GEMINI_API_KEY   - required
  AI_MODEL         - optional override (or use GEMINI_MODEL)

Notes:
  - If `program.py` runs successfully, the fixer stops and prints stdout.
  - If Gemini SDK is missing, the script will explain how to install it.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple


THIS_DIR = Path(__file__).resolve().parent
PROGRAM_FILE = THIS_DIR / "program.py"


def _strip_quotes(value: str) -> str:
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def _load_env_file(path: Path, override: bool = False) -> bool:
    """Load simple KEY=VALUE lines from a .env file into os.environ.

    Returns True if the file existed and was parsed.
    """
    if not path.exists():
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return False
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = _strip_quotes(val.strip())
        if override or key not in os.environ:
            os.environ[key] = val
    return True


def load_env_from_common_locations() -> None:
    """Load .env files from current directory and its parent if present."""
    candidates = [
        THIS_DIR / ".env",
        THIS_DIR / ".env.local",
        THIS_DIR.parent / ".env",
        THIS_DIR.parent / ".env.local",
    ]
    for p in candidates:
        _load_env_file(p, override=False)


def run_program(timeout_seconds: Optional[int] = None) -> Tuple[int, str, str]:
    """Run `program.py` as a child process and capture stdout/stderr.

    Returns (returncode, stdout, stderr).
    """
    if not PROGRAM_FILE.exists():
        return (127, "", f"Missing program file: {PROGRAM_FILE}")

    command = [sys.executable, str(PROGRAM_FILE.name)]
    process = subprocess.Popen(
        command,
        cwd=str(THIS_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        return (124, stdout or "", stderr or "Timed out running program.py")
    return (process.returncode, stdout or "", stderr or "")


def read_program_source() -> str:
    try:
        return PROGRAM_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def build_prompt(code: str, error_text: str) -> str:
    """Create the AI prompt containing the source code and the error message."""
    prompt = (
        "You are an expert software engineer.\n"
        "Task: Fix the provided Python program so it runs without errors.\n"
        "Rules:\n"
        "- Return ONLY the full corrected contents of program.py.\n"
        "- Do not include explanations, comments, or markdown fences.\n"
        "- Preserve functionality; if unclear, choose the simplest working fix.\n"
        "\n"
        "--- BEGIN ERROR OUTPUT ---\n"
        f"{error_text}\n"
        "--- END ERROR OUTPUT ---\n"
        "\n"
        "--- BEGIN program.py ---\n"
        f"{code}\n"
        "--- END program.py ---\n"
    )
    return prompt


class AIClient:
    """Thin wrapper over Gemini (Gemini-only)."""

    def __init__(self, provider: str = "gemini", model: str = "auto") -> None:
        self.provider = "gemini"
        self.model = self._choose_model(model)

    def _choose_model(self, requested: str) -> str:
        if requested != "auto":
            return requested
        env_model = os.environ.get("AI_MODEL")
        if env_model:
            return env_model
        return os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")

    def generate(self, prompt: str) -> str:
        return self._generate_with_gemini(prompt)

    # --- Provider implementations ---
    def _generate_with_gemini(self, prompt: str) -> str:
        try:
            import google.generativeai as genai  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "Gemini SDK not installed. Install with: pip install google-generativeai"
            ) from exc

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set in environment")

        genai.configure(api_key=api_key)
        model_name = self.model or "gemini-1.5-flash"

        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            # The SDK returns candidates; .text gives best combined output.
            text = getattr(response, "text", None) or ""
            if not text and getattr(response, "candidates", None):
                # Fallback if .text missing; concatenate parts
                parts = []
                for c in response.candidates:
                    for p in getattr(c.content, "parts", []) or []:
                        parts.append(getattr(p, "text", ""))
                text = "\n".join([p for p in parts if p])
            return text.strip()
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(f"Gemini generation failed: {exc}") from exc

    # OpenAI support removed (Gemini-only)


CODE_BLOCK_RE = re.compile(r"```[a-zA-Z0-9_\-]*\n([\s\S]*?)```", re.MULTILINE)


def extract_code_from_ai_response(text: str) -> str:
    """Return pure code if the AI wrapped it in markdown; otherwise, raw text."""
    if not text:
        return ""
    match = CODE_BLOCK_RE.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()


def overwrite_program(new_code: str) -> None:
    PROGRAM_FILE.write_text(new_code, encoding="utf-8")


def is_python_exception_error(text: str) -> bool:
    """Heuristic to decide if stderr looks like a Python exception.

    We only auto-fix when a real exception/traceback is present.
    """
    if not text:
        return False
    if "Traceback (most recent call last):" in text:
        return True
    if re.search(r"(Error|Exception)(:|\b)", text, flags=re.IGNORECASE):
        return True
    return False


def main() -> int:
    # Load .env before reading args so environment-driven defaults work
    load_env_from_common_locations()

    parser = argparse.ArgumentParser(description="Run and auto-fix program.py with AI")
    parser.add_argument("--max-attempts", type=int, default=5, help="Max fix attempts")
    parser.add_argument("--timeout", type=int, default=30, help="Seconds to wait for program run")
    parser.add_argument(
        "--model",
        type=str,
        default="auto",
        help="Gemini model name or 'auto'",
    )
    args = parser.parse_args()

    # If user left provider/model as auto, allow .env overrides
    if args.provider == "auto" and os.environ.get("AI_PROVIDER"):
        args.provider = os.environ.get("AI_PROVIDER", "auto").lower()
    if args.model == "auto" and os.environ.get("AI_MODEL"):
        args.model = os.environ.get("AI_MODEL", "auto")

    if not PROGRAM_FILE.exists():
        print(f"Creating missing {PROGRAM_FILE.name} with a simple template...")
        PROGRAM_FILE.write_text("print('Hello from program.py')\n", encoding="utf-8")

    client = AIClient(provider=args.provider, model=args.model)

    for attempt in range(1, args.max_attempts + 1):
        print(f"\n=== Run attempt {attempt} ===")
        returncode, stdout, stderr = run_program(timeout_seconds=args.timeout)

        if returncode == 0 and not stderr.strip():
            print("program.py ran successfully. Output:\n")
            if stdout:
                print(stdout, end="" if stdout.endswith("\n") else "\n")
            else:
                print("(no output)")
            return 0

        # Handle timeout without modifying code
        if returncode == 124:
            print("program.py timed out. Not modifying code. Consider increasing --timeout.")
            return 124

        # If there's no stderr content, don't attempt AI fix
        if not stderr.strip():
            print(f"program.py exited with code {returncode} but no error output. Not modifying code.")
            return returncode

        print("program.py failed. Captured stderr:\n")
        print(stderr)

        # Only fix when stderr looks like a Python exception/traceback
        if not is_python_exception_error(stderr):
            print("Stderr does not look like a Python exception. Not modifying code.")
            return 1

        code = read_program_source()
        prompt = build_prompt(code=code, error_text=stderr or f"exit code {returncode}")

        try:
            ai_response = client.generate(prompt)
        except Exception as exc:
            print(f"AI generation error: {exc}")
            print("Aborting. You may need to set API keys or install the SDK.")
            return 2

        fixed_code = extract_code_from_ai_response(ai_response)
        if not fixed_code.strip():
            print("AI returned empty fix. Aborting to avoid wiping your code.")
            return 3

        overwrite_program(fixed_code)
        print("Wrote AI-corrected code to program.py. Re-running...")

    print(f"Reached max attempts ({args.max_attempts}) without success.")
    return 1


if __name__ == "__main__":
    sys.exit(main())


