#!/usr/bin/env python3
"""Read-only syntax, local Markdown link, and publication privacy checks.

This is a targeted working-tree scan, not a guarantee of secret absence or a
Git history audit. Findings identify locations without printing secret values.
"""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKIP = {".git", ".venv", "venv", "replications", "__pycache__", ".pytest_cache", ".matplotlib"}
TEXT = {".py", ".md", ".txt", ".csv", ".json", ".yml", ".yaml", ".svg", ".sha256"}
PATTERNS = {
    "private key": r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "provider credential": r"\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b",
    "credential assignment": r'''(?i)\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[=:]\s*["'][A-Za-z0-9_+/=-]{12,}["']''',
    "bearer credential": r"(?i)\bBearer\s+[A-Za-z0-9._-]{20,}",
    "personal absolute path": r"(?:[A-Za-z]:[\\/](?:Users|Experiments)[\\/]|/(?:home|Users)/[A-Za-z0-9_.-]+/)",
}


def main():
    findings, python_count, link_count, text_count = [], 0, 0, 0
    files = [path for path in ROOT.rglob("*") if path.is_file()
             and not any(part in SKIP for part in path.relative_to(ROOT).parts)]
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if path.name.startswith(".env") and path.name != ".env.example" or path.suffix in {".pem", ".key"}:
            findings.append(f"{relative}: credential file should not be published")
        if path.suffix not in TEXT and not path.name.startswith((".git", "LICENSE", "NOTICE")):
            continue
        text = path.read_text(encoding="utf-8")
        text_count += 1
        if path.suffix == ".py":
            try:
                compile(text, relative, "exec")
                python_count += 1
            except SyntaxError as exc:
                findings.append(f"{relative}:{exc.lineno}: invalid Python syntax")
        for label, pattern in PATTERNS.items():
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{relative}:{line}: {label}")
        for match in re.finditer(r"[A-Za-z0-9_.+-]+@([A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+)", text):
            if not match.group(1).rstrip(".").endswith(".test"):
                findings.append(f"{relative}: non-synthetic email address")
        if path.suffix == ".md":
            # Ignore fenced examples; validate actual inline links and image paths.
            prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
                target = target.strip().strip("<>")
                parts = urlsplit(target)
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                resolved = (path.parent / unquote(parts.path)).resolve()
                link_count += 1
                if not resolved.is_relative_to(ROOT) or not resolved.exists():
                    findings.append(f"{relative}: broken or external local link: {target}")
    if findings:
        print("FAIL:")
        print("\n".join(f"  {finding}" for finding in findings))
        raise SystemExit(1)
    print(f"PASS: {python_count} Python files compile; {link_count} local Markdown links resolve; "
          f"{text_count} text artifacts scanned with no targeted privacy findings.")
    print("Review Git history, licensing, and rendered GitHub pages separately before publication.")


if __name__ == "__main__":
    main()
