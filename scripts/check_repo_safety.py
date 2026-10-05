#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Repository Safety, Secret, Path Hygiene & Manifest Integrity Checker for 7.css
"""

import getpass
import json
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IGNORED_DIRS = {
    ".git",
    ".vs",
    ".vscode",
    "node_modules",
    "dist",
    "build",
    "scratch",
    "reference",
    "temp",
    "assets/extracted",
}

IGNORED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".mp3",
    ".webm",
    ".wav",
    ".ico",
    ".cur",
    ".ani",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".dll",
    ".exe",
    ".msstyles",
    ".wim",
    ".iso",
    ".zip",
    ".7z",
    ".tar",
    ".gz",
}

IGNORED_FILES = {
    "package-lock.json",
}

# Regex patterns for private path hygiene
WINDOWS_USER_PATH_RE = re.compile(
    r"[A-Za-z]:(?:\\{1,4}|/)+(?:Users|Documents and Settings)(?:\\{1,4}|/)+",
    re.IGNORECASE,
)
USER_HOME_PATH_RE = re.compile(
    r"(?:[A-Za-z]:(?:\\{1,4}|/)+|/|\\{1,4})(?:Users|home|Documents and Settings)(?:\\{1,4}|/)+[A-Za-z0-9_.-]+(?:\\{1,4}|/)+",
    re.IGNORECASE,
)
UNIX_USER_PATH_RE = re.compile(r"^/(?:Users|home)/[A-Za-z0-9_.-]+(?:/|$)", re.IGNORECASE)
USER_FILE_URI_RE = re.compile(
    r"file:///(?:[A-Za-z]:/(?:Users|Documents and Settings|home)|(?:Users|home)/)",
    re.IGNORECASE,
)

# Documentation sample paths to allow (e.g. legacy XP.css sample table in listview.ejs)
DOC_SAMPLE_RE = re.compile(r"[A-Za-z]:(?:\\{1,4}|/)+Users(?:\\{1,4}|/)+user(?:\\{1,4}|/)+", re.IGNORECASE)

try:
    CURRENT_USER = getpass.getuser()
    if CURRENT_USER and len(CURRENT_USER) > 1 and CURRENT_USER.lower() not in {"root", "runner", "github", "administrator", "system", "user"}:
        ACTIVE_USER_PATH_RE = re.compile(
            rf"(?:\\{{1,4}}|/)+{re.escape(CURRENT_USER)}(?:\\{{1,4}}|/)+",
            re.IGNORECASE,
        )
    else:
        ACTIVE_USER_PATH_RE = None
except Exception:
    ACTIVE_USER_PATH_RE = None

SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC|DSA|PGP)?\s?PRIVATE KEY-----"), "Private Key Header"),
    (re.compile(r"\b(?:sk|pk)_(?:live|test)_[0-9a-zA-Z]{24,}\b"), "API Key Token"),
    (re.compile(r"\bghp_[0-9a-zA-Z]{36}\b"), "GitHub Personal Access Token"),
    (re.compile(r"\bgho_[0-9a-zA-Z]{36}\b"), "GitHub OAuth Token"),
    (re.compile(r"\bxox[baprs]-[0-9a-zA-Z]{10,48}\b"), "Slack Token"),
    (re.compile(r"\beyJ[a-zA-Z0-9_\-]{20,}\.[a-zA-Z0-9_\-]{20,}\.[a-zA-Z0-9_\-]{20,}\b"), "JWT Token"),
]


def check_file_hygiene(file_path: str, rel_path: str) -> list[str]:
    violations = []
    if rel_path == "scripts/check_repo_safety.py":
        return violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.read().splitlines()

        for line_no, line in enumerate(lines, start=1):
            if DOC_SAMPLE_RE.search(line):
                # Permitted documentation mock path
                continue

            if WINDOWS_USER_PATH_RE.search(line):
                violations.append(f"{rel_path}:{line_no}: Hardcoded Windows user directory path leak: {line.strip()[:100]}")
            if USER_HOME_PATH_RE.search(line):
                violations.append(f"{rel_path}:{line_no}: Hardcoded user profile directory path: {line.strip()[:100]}")
            if UNIX_USER_PATH_RE.search(line):
                violations.append(f"{rel_path}:{line_no}: Hardcoded Unix user home directory path: {line.strip()[:100]}")
            if ACTIVE_USER_PATH_RE and ACTIVE_USER_PATH_RE.search(line):
                violations.append(f"{rel_path}:{line_no}: Active OS user path component: {line.strip()[:100]}")
            if USER_FILE_URI_RE.search(line):
                violations.append(f"{rel_path}:{line_no}: Local user file URI (file:///): {line.strip()[:100]}")

            for pattern, desc in SECRET_PATTERNS:
                if pattern.search(line):
                    violations.append(f"{rel_path}:{line_no}: Potential secret/credential ({desc}): {line.strip()[:60]}...")

    except Exception as ex:
        violations.append(f"{rel_path}: Failed to read file ({ex})")

    return violations


def check_manifest_integrity() -> list[str]:
    violations = []
    manifest_path = os.path.join(REPO_ROOT, "assets", "manifest.json")
    if not os.path.exists(manifest_path):
        return ["assets/manifest.json does not exist."]

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
    except Exception as e:
        return [f"assets/manifest.json is not valid JSON: {e}"]

    if "version" not in manifest_data:
        violations.append("assets/manifest.json missing 'version' field.")
    if "files" not in manifest_data or not isinstance(manifest_data["files"], list):
        violations.append("assets/manifest.json missing 'files' list.")
        return violations

    for item in manifest_data["files"]:
        rel_path = item.get("path")
        if not rel_path:
            violations.append("Item in manifest.json missing 'path' attribute.")
            continue
        full_path = os.path.join(REPO_ROOT, rel_path)
        if not os.path.exists(full_path):
            violations.append(f"Manifest references file that does not exist on disk: {rel_path}")

    return violations


def check_git_tracked_binaries() -> list[str]:
    violations = []
    try:
        res = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        for tracked in res.stdout.splitlines():
            ext = os.path.splitext(tracked)[1].lower()
            if ext in {".dll", ".exe", ".msstyles", ".wim", ".iso", ".zip", ".7z", ".tar", ".gz"}:
                violations.append(f"Tracked forbidden binary file in git: {tracked}")
            if tracked.startswith("scratch/") or tracked.startswith("reference/"):
                violations.append(f"Tracked reference directory file in git: {tracked}")
    except Exception:
        pass
    return violations


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    print(f"Scanning repository for safety, secrets, path hygiene, and manifest integrity: {REPO_ROOT}")
    all_violations = []

    # 1. Manifest integrity check
    print("Checking assets/manifest.json integrity...")
    all_violations.extend(check_manifest_integrity())

    # 2. Git tracked binaries
    print("Checking git tracked file hygiene...")
    all_violations.extend(check_git_tracked_binaries())

    # 3. Path & secret hygiene
    print("Scanning tracked and source files for private path leaks and secrets...")
    for root, dirs, files in os.walk(REPO_ROOT):
        rel_root = os.path.relpath(root, REPO_ROOT).replace("\\", "/")
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and f"{rel_root}/{d}".strip("/") not in IGNORED_DIRS]

        if any(rel_root.startswith(ignored) for ignored in IGNORED_DIRS):
            continue

        for file in files:
            if file in IGNORED_FILES:
                continue

            ext = os.path.splitext(file)[1].lower()
            if ext in IGNORED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, REPO_ROOT).replace("\\", "/")

            violations = check_file_hygiene(file_path, rel_path)
            all_violations.extend(violations)

    if all_violations:
        print(f"\n[FAILED] Found {len(all_violations)} hygiene violation(s):\n")
        for v in all_violations:
            print(f"  - {v}")
        print("\nPlease resolve the above issues before committing or publishing.")
        return 1

    print("\n[PASSED] Zero path leaks, secrets, binary artifacts, or manifest inconsistencies detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
