#!/usr/bin/env python3
"""
scripts/verify_stage_2.py

Automated verification harness for Phase 2 (Form Controls & Command Primitives).
Validates:
  1. SCSS Form Control Rebuilds: validates _button.scss, _checkbox.scss, _radiobutton.scss,
     _textbox.scss, _groupbox.scss, _slider.scss, _spinner.scss
  2. Authentic Windows 7 Aero Features: verifies 6-state buttons, pulse animations, command links,
     SVG vector masks for checkboxes and radio bullets, and spin controls
  3. Built Artifact Validation: verifies dist/7.css, dist/7.scoped.css, dist/7.inline.css
  4. Repository Safety & Secret Audit: invokes check_repo_safety.py
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


def test_button_scss():
    btn_path = ROOT_DIR / "gui" / "_button.scss"
    check("_button.scss exists", btn_path.is_file())
    content = btn_path.read_text(encoding="utf-8")

    check("_button.scss references --w7-btn-bg", "--w7-btn-bg" in content)
    check("_button.scss references --w7-btn-default-bg", "--w7-btn-default-bg" in content)
    check("_button.scss references --w7-btn-hover-bg", "--w7-btn-hover-bg" in content)
    check("_button.scss references --w7-btn-pressed-bg", "--w7-btn-pressed-bg" in content)
    check("_button.scss references --w7-btn-disabled-bg", "--w7-btn-disabled-bg" in content)
    check("_button.scss binds default pulse animation", "w7-aero-button-pulse" in content)
    check("_button.scss implements .command-link", ".command-link" in content)
    check("_button.scss embeds command link arrow vector", "command-link-arrow.svg" in content)
    check("_button.scss contains Vista button styling", "--w7-vista-btn-bg" in content)
    check("_button.scss binds Vista button pulse", "w7-vista-button-pulse" in content)


def test_checkbox_radio_scss():
    cb_path = ROOT_DIR / "gui" / "_checkbox.scss"
    rad_path = ROOT_DIR / "gui" / "_radiobutton.scss"
    check("_checkbox.scss exists", cb_path.is_file())
    check("_radiobutton.scss exists", rad_path.is_file())

    cb_content = cb_path.read_text(encoding="utf-8")
    check("_checkbox.scss references --w7-checkbox-bg", "--w7-checkbox-bg" in cb_content)
    check("_checkbox.scss handles :checked", ":checked" in cb_content)
    check("_checkbox.scss handles :indeterminate", ":indeterminate" in cb_content)
    check("_checkbox.scss embeds checkbox checkmark vector", "checkbox-check.svg" in cb_content)
    check("_checkbox.scss embeds indeterminate glyph vector", "checkbox-indeterminate.svg" in cb_content)
    check("_checkbox.scss contains Vista theme overrides", '[data-theme="vista"]' in cb_content)

    rad_content = rad_path.read_text(encoding="utf-8")
    check("_radiobutton.scss references --w7-radio-bg", "--w7-radio-bg" in rad_content)
    check("_radiobutton.scss handles :checked", ":checked" in rad_content)
    check("_radiobutton.scss embeds radio bullet vector", "radio-bullet.svg" in rad_content)
    check("_radiobutton.scss contains Vista theme overrides", '[data-theme="vista"]' in rad_content)


def test_input_groupbox_scss():
    tb_path = ROOT_DIR / "gui" / "_textbox.scss"
    gb_path = ROOT_DIR / "gui" / "_groupbox.scss"
    check("_textbox.scss exists", tb_path.is_file())
    check("_groupbox.scss exists", gb_path.is_file())

    tb_content = tb_path.read_text(encoding="utf-8")
    check("_textbox.scss references --w7-input-border", "--w7-input-border" in tb_content)
    check("_textbox.scss references --w7-input-border-focus", "--w7-input-border-focus" in tb_content)
    check("_textbox.scss handles textarea", "textarea" in tb_content)
    check("_textbox.scss contains Vista focus styling", '[data-theme="vista"]' in tb_content)

    gb_content = gb_path.read_text(encoding="utf-8")
    check("_groupbox.scss references --w7-groupbox-border", "--w7-groupbox-border" in gb_content)
    check("_groupbox.scss references --w7-groupbox-legend-color", "--w7-groupbox-legend-color" in gb_content)


def test_slider_spinner_scss():
    slider_path = ROOT_DIR / "gui" / "_slider.scss"
    spinner_path = ROOT_DIR / "gui" / "_spinner.scss"
    check("_slider.scss exists", slider_path.is_file())
    check("_spinner.scss exists", spinner_path.is_file())

    sl_content = slider_path.read_text(encoding="utf-8")
    check("_slider.scss references --w7-slider-track-bg", "--w7-slider-track-bg" in sl_content)
    check("_slider.scss references --w7-slider-thumb-bg", "--w7-slider-thumb-bg" in sl_content)
    check("_slider.scss styles -webkit-slider-thumb", "-webkit-slider-thumb" in sl_content)
    check("_slider.scss styles -moz-range-thumb", "-moz-range-thumb" in sl_content)
    check("_slider.scss contains Vista slider thumb overrides", '[data-theme="vista"]' in sl_content)

    sp_content = spinner_path.read_text(encoding="utf-8")
    check("_spinner.scss implements .spin-box", ".spin-box" in sp_content)
    check("_spinner.scss implements .spin-up and .spin-down", ".spin-up" in sp_content and ".spin-down" in sp_content)
    check("_spinner.scss embeds spin arrows", "spin-arrow-up.svg" in sp_content and "spin-arrow-down.svg" in sp_content)
    check("_spinner.scss contains Vista button overrides", '[data-theme="vista"]' in sp_content)


def test_progressbar_scss():
    pb_path = ROOT_DIR / "gui" / "_progressbar.scss"
    check("_progressbar.scss exists", pb_path.is_file())
    pb_content = pb_path.read_text(encoding="utf-8")
    check("_progressbar.scss implements progressbar role", '[role="progressbar"]' in pb_content)
    check("_progressbar.scss contains Vista Aurora progress bar styling", '[data-theme="vista"]' in pb_content)


def test_dropdown_combobox_listbox_scss():
    dd_path = ROOT_DIR / "gui" / "_dropdown.scss"
    cb_path = ROOT_DIR / "gui" / "_combobox.scss"
    lb_path = ROOT_DIR / "gui" / "_listbox.scss"
    check("_dropdown.scss exists", dd_path.is_file())
    check("_combobox.scss exists", cb_path.is_file())
    check("_listbox.scss exists", lb_path.is_file())

    dd_content = dd_path.read_text(encoding="utf-8")
    check("_dropdown.scss references --w7-combobox-btn-bg", "--w7-combobox-btn-bg" in dd_content)
    check("_dropdown.scss embeds dropdown arrow", "dropdown-arrow.svg" in dd_content)
    check("_dropdown.scss contains Vista theme overrides", '[data-theme="vista"]' in dd_content)

    cb_content = cb_path.read_text(encoding="utf-8")
    check("_combobox.scss implements .combobox", ".combobox" in cb_content)
    check("_combobox.scss references --w7-metric-combobox-btn-width", "--w7-metric-combobox-btn-width" in cb_content)
    check("_combobox.scss contains Vista theme overrides", '[data-theme="vista"]' in cb_content)

    lb_content = lb_path.read_text(encoding="utf-8")
    check("_listbox.scss references --w7-listbox-border", "--w7-listbox-border" in lb_content)
    check("_listbox.scss references --w7-listbox-selected-bg", "--w7-listbox-selected-bg" in lb_content)
    check("_listbox.scss contains Vista theme overrides", '[data-theme="vista"]' in lb_content)


def test_build_artifacts():
    dist_dir = ROOT_DIR / "dist"
    for bundle_name in ["7.css", "7.scoped.css", "7.inline.css"]:
        bundle = dist_dir / bundle_name
        check(f"dist/{bundle_name} exists", bundle.is_file())
        content = bundle.read_text(encoding="utf-8")
        check(f"dist/{bundle_name} contains command-link", "command-link" in content)
        check(f"dist/{bundle_name} contains spin-box", "spin-box" in content)
        check(f"dist/{bundle_name} contains range slider", "slider" in content or "range" in content)
        check(f"dist/{bundle_name} contains vista theme rules", "vista" in content)


def test_safety_check():
    safety_script = ROOT_DIR / "scripts" / "check_repo_safety.py"
    check("Safety script exists", safety_script.is_file())
    res = subprocess.run([sys.executable, str(safety_script)], cwd=str(ROOT_DIR), capture_output=True, text=True)
    check("Safety audit script passes with zero violations", res.returncode == 0, res.stdout + res.stderr)


def main():
    print("=== PHASE 2 VERIFICATION AUDIT ===")
    test_button_scss()
    test_checkbox_radio_scss()
    test_input_groupbox_scss()
    test_slider_spinner_scss()
    test_progressbar_scss()
    test_dropdown_combobox_listbox_scss()
    test_build_artifacts()
    test_safety_check()
    print("=== ALL PHASE 2 CHECKS PASSED ===")


if __name__ == "__main__":
    main()
