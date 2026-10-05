#!/usr/bin/env python3
"""
scripts/verify_stage_1.py

Automated verification harness for Phase 1 (Token Architecture & Color Engine).
Validates:
  1. JSON Token Integrity: checks all 6 schema files in assets/tokens/
  2. SCSS Token Generation: validates _tokens.scss, _aero-tints.scss, _variables.scss
  3. 16-Color Aero Matrix: validates exact selector and attribute coverage
  4. Typography Scale & Smoothing: validates subpixel rendering declarations
  5. Built Artifact Validation: verifies dist/7.css, dist/7.scoped.css, dist/7.inline.css
  6. Repository Safety & Secret Audit: invokes check_repo_safety.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def check(description: str, condition: bool, details: str = ""):
    if condition:
        print(f"[PASS] {description}")
    else:
        print(f"[FAIL] {description} - {details}")
        sys.exit(1)


def test_json_tokens():
    tokens_dir = ROOT_DIR / "assets" / "tokens"
    required_files = [
        "colors.json",
        "metrics.json",
        "typography.json",
        "animations.json",
        "aero_math.json",
        "slices.json",
    ]
    for filename in required_files:
        path = tokens_dir / filename
        check(f"Token file exists: {filename}", path.is_file())
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            check(f"Token file parses valid JSON: {filename}", isinstance(data, dict))


def test_generated_scss():
    tokens_scss = ROOT_DIR / "gui" / "_tokens.scss"
    tints_scss = ROOT_DIR / "gui" / "_aero-tints.scss"
    variables_scss = ROOT_DIR / "gui" / "_variables.scss"

    check("_tokens.scss exists", tokens_scss.is_file())
    check("_aero-tints.scss exists", tints_scss.is_file())
    check("_variables.scss exists", variables_scss.is_file())

    tokens_content = tokens_scss.read_text(encoding="utf-8")
    tints_content = tints_scss.read_text(encoding="utf-8")
    vars_content = variables_scss.read_text(encoding="utf-8")

    # Key tokens in _tokens.scss
    expected_vars = [
        "--w7-font-family",
        "--w7-font-rendering",
        "--w7-color-window-bg",
        "--w7-color-window-text",
        "--w7-glass-blur",
        "--w7-glass-specular-angle",
        "--w7-aero-tint-color",
        "--w7-btn-bg",
        "--w7-btn-hover-bg",
        "--w7-btn-pressed-bg",
        "--w7-btn-default-pulse-bg",
        "--w7-progress-normal-chunk",
        "--w7-basic-title-active-bg",
        "--w7-metric-window-border-width",
        "--w7-metric-btn-height",
        "--w7-ease-fast-entrance",
        "--w7-dur-btn-pulse",
    ]
    for var_name in expected_vars:
        check(f"_tokens.scss declares {var_name}", var_name in tokens_content)

    # Keyframes in _tokens.scss
    check("_tokens.scss has button pulse keyframes", "@keyframes w7-aero-button-pulse" in tokens_content)
    check("_tokens.scss has progress shimmer keyframes", "@keyframes w7-progress-shimmer" in tokens_content)

    # 16 tints in _aero-tints.scss
    tints = [
        "default", "sky", "twilight", "smoke", "pink", "frost", "blush",
        "ruby", "pumpkin", "sun", "lime", "leaf", "sea", "violet", "fuchsia", "slate"
    ]
    for tint in tints:
        check(f"_aero-tints.scss contains tint '{tint}'", f'[data-aero-tint="{tint}"]' in tints_content)

    # Basic and high-contrast fallbacks
    check("_aero-tints.scss has basic theme fallback", '[data-theme="basic"]' in tints_content)
    check("_aero-tints.scss has high-contrast fallback", '[data-theme="high-contrast"]' in tints_content)

    # Legacy mappings in _variables.scss
    check("_variables.scss imports _tokens.scss", '@import "_tokens.scss";' in vars_content)
    check("_variables.scss imports _aero-tints.scss", '@import "_aero-tints.scss";' in vars_content)
    check("_variables.scss provides --w7-el-bg legacy alias", "--w7-el-bg:" in vars_content)
    check("_variables.scss provides --w7-el-grad legacy alias", "--w7-el-grad:" in vars_content)


def test_typography_scss():
    typo_scss = ROOT_DIR / "gui" / "_typography.scss"
    check("_typography.scss exists", typo_scss.is_file())
    content = typo_scss.read_text(encoding="utf-8")

    check("_typography.scss applies subpixel smoothing", "-webkit-font-smoothing: var(--w7-font-smoothing-webkit);" in content)
    check("_typography.scss applies text-rendering", "text-rendering: var(--w7-font-rendering);" in content)
    check("_typography.scss defines .instruction-primary", ".instruction" in content and "-primary" in content)


def test_build_artifacts():
    dist_dir = ROOT_DIR / "dist"
    check("dist/7.css exists", (dist_dir / "7.css").is_file())
    check("dist/7.scoped.css exists", (dist_dir / "7.scoped.css").is_file())
    check("dist/7.inline.css exists", (dist_dir / "7.inline.css").is_file())
    check("dist/gui directory exists", (dist_dir / "gui").is_dir())

    css_content = (dist_dir / "7.css").read_text(encoding="utf-8")
    check("dist/7.css contains --w7-font-family", "--w7-font-family" in css_content)
    check("dist/7.css contains --w7-glass-blur", "--w7-glass-blur" in css_content)
    check("dist/7.css contains aero tints", "data-aero-tint=default" in css_content or 'data-aero-tint="default"' in css_content)


def test_safety_check():
    safety_script = ROOT_DIR / "scripts" / "check_repo_safety.py"
    check("Safety script exists", safety_script.is_file())
    res = subprocess.run([sys.executable, str(safety_script)], cwd=str(ROOT_DIR), capture_output=True, text=True)
    check("Safety audit script passes with zero violations", res.returncode == 0, res.stdout + res.stderr)


def main():
    print("=== PHASE 1 VERIFICATION AUDIT ===")
    test_json_tokens()
    test_generated_scss()
    test_typography_scss()
    test_build_artifacts()
    test_safety_check()
    print("=== ALL PHASE 1 CHECKS PASSED ===")


if __name__ == "__main__":
    main()
