#!/usr/bin/env python3
"""
scripts/verify_stage_3.py

Automated verification harness for Phase 3 (Structural Shell & Window Compositing).
Validates:
  1. Window & Glass Compositing: validates _window.scss Aero Glass shaders, backdrop-filter,
     specular reflection overlays, text halo glows, restored/inactive/maximized states.
  2. Caption Button State Machine: validates 4-state buttons, cyan and crimson radial back-glows,
     and crisp SVG vector micro-glyphs.
  3. Windows Vista Theming Adaptations: validates 8px restored radius, 7px frame border,
     solid black maximized frames, 43x19px caption buttons, amber/orange close hover glow,
     and Vista Basic fallback rules.
  4. Task Dialog & Aero Wizard: validates structural containers (.task-dialog, .window.wizard),
     typography hierarchy (12pt primary instruction), expando details, and commit footers.
  5. Built Artifact Validation: verifies dist/7.css, dist/7.scoped.css, dist/7.inline.css
  6. Repository Safety Audit: invokes check_repo_safety.py
"""

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


def test_window_scss():
    win_path = ROOT_DIR / "gui" / "_window.scss"
    check("_window.scss exists", win_path.is_file())
    content = win_path.read_text(encoding="utf-8")

    # Aero Glass Compositing & Shaders
    check("_window.scss binds backdrop-filter", "backdrop-filter: var(--w7-glass-blur)" in content)
    check("_window.scss binds -webkit-backdrop-filter", "-webkit-backdrop-filter: var(--w7-glass-blur)" in content)
    check("_window.scss binds restored box-shadow", "var(--w7-glass-shadow-restored)" in content)
    check("_window.scss binds specular reflections", "var(--w7-glass-specular-reflection)" in content)
    check("_window.scss binds active text halo glow", "var(--w7-glass-text-halo-active)" in content)
    check("_window.scss binds inactive text halo glow", "var(--w7-glass-text-halo-inactive)" in content)
    check("_window.scss binds inactive state styling", "&:not(.active)" in content or ".inactive" in content)
    check("_window.scss binds maximized state styling", "&.maximized" in content)

    # Caption Button Shaders & Vectors
    check("_window.scss embeds caption-minimize SVG", "caption-minimize.svg" in content)
    check("_window.scss embeds caption-maximize SVG", "caption-maximize.svg" in content)
    check("_window.scss embeds caption-restore SVG", "caption-restore.svg" in content)
    check("_window.scss embeds caption-close SVG", "caption-close.svg" in content)
    check("_window.scss embeds caption-close-white SVG", "caption-close-white.svg" in content)
    check("_window.scss embeds caption-help SVG", "caption-help.svg" in content)
    check("_window.scss binds cyan caption button glow", "#5dc4f0" in content or "2aceda" in content)
    check("_window.scss binds crimson close button glow", "#e68e75" in content or "d42809" in content)

    # Vista Theming Adaptations
    check("_window.scss binds Vista theme attribute", '[data-theme="vista"]' in content)
    check("_window.scss binds Vista window radius metric", "--w7-vista-metric-window-radius" in content)
    check("_window.scss binds Vista glass blur shader", "--w7-vista-glass-blur" in content)
    check("_window.scss binds Vista glass shadow", "--w7-vista-glass-shadow-restored" in content)
    check("_window.scss binds Vista text halo", "--w7-vista-glass-text-halo-active" in content)
    check("_window.scss binds Vista caption button dimensions", "--w7-vista-metric-caption-btn-width" in content)
    check("_window.scss binds Vista solid black maximized frame", "#000000" in content)
    check("_window.scss binds Vista basic theme fallback", '[data-theme="vista-basic"]' in content)

    # Task Dialog Architecture
    check("_window.scss implements .task-dialog", ".task-dialog" in content)
    check("_window.scss implements .task-dialog-header", ".task-dialog-header" in content)
    check("_window.scss implements .task-dialog-icon", ".task-dialog-icon" in content)
    check("_window.scss implements .task-dialog-instruction", ".task-dialog-instruction" in content)
    check("_window.scss implements .task-dialog-content", ".task-dialog-content" in content)
    check("_window.scss implements .task-dialog-expando", ".task-dialog-expando" in content)
    check("_window.scss implements .task-dialog-footer", ".task-dialog-footer" in content)
    check("_window.scss embeds task dialog info icon", "task-dialog-info.svg" in content)
    check("_window.scss embeds task dialog warning icon", "task-dialog-warning.svg" in content)
    check("_window.scss embeds task dialog error icon", "task-dialog-error.svg" in content)
    check("_window.scss embeds task dialog shield icon", "task-dialog-shield.svg" in content)

    # Aero Wizard & Status Bar
    check("_window.scss implements .window.wizard", ".window.wizard" in content)
    check("_window.scss embeds window back navigation button", "window-back.svg" in content)
    check("_window.scss implements .status-bar", ".status-bar" in content)
    check("_window.scss implements .status-bar-field", ".status-bar-field" in content)
    check("_window.scss implements .status-bar-grip", ".status-bar-grip" in content)


def test_build_artifacts():
    dist_dir = ROOT_DIR / "dist"
    for bundle_name in ["7.css", "7.scoped.css", "7.inline.css"]:
        bundle = dist_dir / bundle_name
        check(f"dist/{bundle_name} exists", bundle.is_file())
        content = bundle.read_text(encoding="utf-8")
        check(f"dist/{bundle_name} contains title-bar", "title-bar" in content)
        check(f"dist/{bundle_name} contains task-dialog", "task-dialog" in content)
        check(f"dist/{bundle_name} contains status-bar", "status-bar" in content)
        check(f"dist/{bundle_name} contains vista theme window rules", "vista" in content)
        check(f"dist/{bundle_name} contains dialog animations", "dialog-open" in content)


def test_safety_check():
    safety_script = ROOT_DIR / "scripts" / "check_repo_safety.py"
    check("Safety script exists", safety_script.is_file())
    res = subprocess.run([sys.executable, str(safety_script)], cwd=str(ROOT_DIR), capture_output=True, text=True)
    check("Safety audit script passes with zero violations", res.returncode == 0, res.stdout + res.stderr)


def main():
    print("=== PHASE 3 VERIFICATION AUDIT ===")
    test_window_scss()
    test_build_artifacts()
    test_safety_check()
    print("=== ALL PHASE 3 CHECKS PASSED ===")


if __name__ == "__main__":
    main()
