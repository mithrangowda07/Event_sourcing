#!/usr/bin/env python3
"""
AI Project Fixer (Gemini-only)

Iteratively runs a command (tests/app), captures Python errors, identifies the
first in-repo file from the traceback, asks Gemini to fix that file, applies
the edit, and repeats until success or max attempts reached.

Typical usage:
  python ai_fix_project.py --command "python -m pytest" --max-attempts 5

Environment variables (optional):
  GEMINI_API_KEY, AI_MODEL (or GEMINI_MODEL)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parent


def _strip_quotes(value: str) -> str:
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def _load_env_file(path: Path, override: bool = False) -> bool:
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
    candidates = [
        PROJECT_ROOT / ".env",
        PROJECT_ROOT / ".env.local",
    ]
    for p in candidates:
        _load_env_file(p, override=False)


@dataclass
class TracebackFrame:
    file_path: Path
    line_number: int
    function_name: str


TRACEBACK_RE = re.compile(
    r"File \"(?P<file>.+?)\", line (?P<line>\d+), in (?P<func>[^\n\r]+)"
)


def parse_traceback(stderr_text: str) -> List[TracebackFrame]:
    frames: List[TracebackFrame] = []
    for match in TRACEBACK_RE.finditer(stderr_text):
        try:
            file_str = match.group("file")
            line_num = int(match.group("line"))
            func = match.group("func").strip()
            frames.append(
                TracebackFrame(file_path=Path(file_str).resolve(), line_number=line_num, function_name=func)
            )
        except Exception:
            continue
    return frames


def filter_in_repo_frames(frames: List[TracebackFrame]) -> List[TracebackFrame]:
    in_repo: List[TracebackFrame] = []
    for fr in frames:
        try:
            fr_rel = fr.file_path.relative_to(PROJECT_ROOT)
        except Exception:
            continue
        # Exclude virtual envs and site-packages
        parts = {p.lower() for p in fr_rel.parts}
        if any(x in parts for x in {"site-packages", "dist-packages", "__pycache__"}):
            continue
        in_repo.append(fr)
    return in_repo


def run_command(command: str, timeout_seconds: Optional[int]) -> Tuple[int, str, str]:
    proc = subprocess.Popen(
        command if os.name == "nt" else shlex.split(command),
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        shell=os.name == "nt",
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        return (124, stdout or "", stderr or "Timed out")
    return (proc.returncode, stdout or "", stderr or "")


class AIClient:
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

    def _generate_with_gemini(self, prompt: str) -> str:
        try:
            import google.generativeai as genai  # type: ignore
        except Exception as exc:
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
            text = getattr(response, "text", None) or ""
            if not text and getattr(response, "candidates", None):
                parts = []
                for c in response.candidates:
                    for p in getattr(c.content, "parts", []) or []:
                        parts.append(getattr(p, "text", ""))
                text = "\n".join([p for p in parts if p])
            return text.strip()
        except Exception as exc:
            raise RuntimeError(f"Gemini generation failed: {exc}") from exc

    # OpenAI support intentionally removed (Gemini-only)


CODE_BLOCK_RE = re.compile(r"```[a-zA-Z0-9_\-]*\n([\s\S]*?)```", re.MULTILINE)


def extract_code_from_ai_response(text: str) -> str:
    if not text:
        return ""
    match = CODE_BLOCK_RE.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()


def build_prompt_for_file_fix(file_path: Path, file_source: str, error_text: str) -> str:
    rel = file_path.relative_to(PROJECT_ROOT)
    return (
        "You are an expert Python engineer.\n"
        "Task: Fix the provided file so the command runs without errors.\n"
        "Rules:\n"
        "- Return ONLY the full corrected contents of the file.\n"
        "- Do not include explanations, comments, or markdown fences.\n"
        "- Preserve functionality; if unclear, choose the simplest working fix.\n"
        f"\n--- BEGIN ERROR OUTPUT ---\n{error_text}\n--- END ERROR OUTPUT ---\n"
        f"\n--- BEGIN {rel.as_posix()} ---\n{file_source}\n--- END {rel.as_posix()} ---\n"
    )


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def choose_target_file(stderr_text: str) -> Optional[Path]:
    frames = parse_traceback(stderr_text)
    in_repo = filter_in_repo_frames(frames)
    if not in_repo:
        return None
    # Choose the last frame in repo (closest to the error source)
    return in_repo[-1].file_path


def main() -> int:
    load_env_from_common_locations()

    parser = argparse.ArgumentParser(description="Run a command and auto-fix project files with Gemini")
    parser.add_argument("--command", required=True, help="Command to run (e.g., 'python -m pytest')")
    parser.add_argument("--max-attempts", type=int, default=5, help="Max fix attempts")
    parser.add_argument("--timeout", type=int, default=180, help="Seconds to wait for command")
    parser.add_argument("--provider", type=str, default="gemini", choices=["gemini"], help="AI provider (Gemini only)")
    parser.add_argument("--model", type=str, default="auto", help="Gemini model name or 'auto'")
    args = parser.parse_args()

    client = AIClient(provider="gemini", model=args.model)

    for attempt in range(1, args.max_attempts + 1):
        print(f"\n=== Run attempt {attempt} ===")
        code, stdout, stderr = run_command(args.command, timeout_seconds=args.timeout)

        if code == 0 and not stderr.strip():
            print("✅ Command succeeded with no errors. Output:\n")
            if stdout:
                print(stdout, end="" if stdout.endswith("\n") else "\n")
            else:
                print("(no output)")
            return 0

        if code == 124:
            print("⏱️ Command timed out. Not modifying code. Consider increasing --timeout.")
            return 124

        if not stderr.strip():
            print(f"Command exited with code {code} but no error output. Not modifying code.")
            return code

        print("❌ Command failed. Captured stderr:\n")
        print(stderr)

        target = choose_target_file(stderr)
        if not target:
            print("ℹ️ Could not identify an in-repo file from traceback. Aborting.")
            return 1

        if not target.exists():
            print(f"ℹ️ Target file not found: {target}")
            return 1

        source = read_text(target)
        if not source.strip():
            print(f"ℹ️ Target file is empty or unreadable: {target}")
            return 1

        prompt = build_prompt_for_file_fix(target, source, stderr)
        try:
            ai_response = client.generate(prompt)
        except Exception as exc:
            print(f"AI generation error: {exc}")
            print("Aborting. You may need to set API keys or install the SDK.")
            return 2

        fixed = extract_code_from_ai_response(ai_response)
        if not fixed.strip():
            print("AI returned empty fix. Aborting to avoid wiping your code.")
            return 3

        write_text(target, fixed)
        rel = target.relative_to(PROJECT_ROOT)
        print(f"📝 Wrote AI-corrected code to {rel}. Re-running...")

    print(f"Reached max attempts ({args.max_attempts}) without success.")
    return 1


if __name__ == "__main__":
    sys.exit(main())


