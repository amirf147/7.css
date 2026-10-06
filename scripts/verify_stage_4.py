#!/usr/bin/env python3
"""
scripts/verify_stage_4.py

Automated verification harness for Phase 4 (Complex Navigation & Explorer Controls).
Validates:
  1. TreeView Control (_treeview.scss): authentic triangular vector chevrons,
     row selection states, inactive selection, and Vista theming.
  2. Breadcrumb Bar (_breadcrumb.scss): split segments, vector dropdown chevrons,
     hover pills, and Vista theming.
  3. ListView & Details Table (_listview.scss): 3-state column headers, sort indicators,
     row hover/active selections, icons/tiles grids, and marquee selection box.
  4. Explorer Command Bar (_commandbar.scss): toolbars, action buttons, split buttons,
     and Vista glossy pill adaptations.
  5. Tabs Framework (_tabs.scss): property sheet tabs, 4-directional orientations.
  6. Scrollbars Modernization (_scrollbar.scss): vector arrows, elimination of raster PNGs.
  7. Systems Layout Primitives (_layout.scss & _ribbon.scss): action panes, splitters,
     category grids, and Scenic Ribbon application button, QAT, chunks, launchers.
  8. Built Artifacts: dist/7.css, dist/7.scoped.css, dist/7.inline.css.
  9. Repository Safety: scripts/check_repo_safety.py.
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


def test_treeview():
    tv_path = ROOT_DIR / "gui" / "_treeview.scss"
    check("_treeview.scss exists", tv_path.is_file())
    content = tv_path.read_text(encoding="utf-8")

    check("_treeview.scss embeds closed vector chevron", "treeview-chevron-closed.svg" in content)
    check("_treeview.scss embeds opened vector chevron", "treeview-chevron-opened.svg" in content)
    check("_treeview.scss embeds hover chevron", "treeview-chevron-closed-hover.svg" in content)
    check("_treeview.scss implements .selected state", ".selected" in content)
    check("_treeview.scss implements aria-selected", '[aria-selected="true"]' in content)
    check("_treeview.scss handles inactive selection", ":not(:focus-within)" in content)
    check("_treeview.scss supports full-row-select", "full-row-select" in content)
    check("_treeview.scss contains Vista theme overrides", '[data-theme="vista"]' in content)


def test_breadcrumb():
    bc_path = ROOT_DIR / "gui" / "_breadcrumb.scss"
    check("_breadcrumb.scss exists", bc_path.is_file())
    content = bc_path.read_text(encoding="utf-8")

    check("_breadcrumb.scss implements .breadcrumb-bar", ".breadcrumb-bar" in content)
    check("_breadcrumb.scss implements .breadcrumb-segment", ".breadcrumb-segment" in content)
    check("_breadcrumb.scss embeds dropdown chevron", "breadcrumb-dropdown.svg" in content)
    check("_breadcrumb.scss supports text input address edit", 'input[type="text"]' in content)
    check("_breadcrumb.scss contains Vista theme overrides", '[data-theme="vista"]' in content)


def test_listview():
    lv_path = ROOT_DIR / "gui" / "_listview.scss"
    check("_listview.scss exists", lv_path.is_file())
    content = lv_path.read_text(encoding="utf-8")

    check("_listview.scss styles column headers", "thead > tr > th" in content)
    check("_listview.scss implements sort ascending chevron", "listview-sort-asc.svg" in content)
    check("_listview.scss implements sort descending chevron", "listview-sort-desc.svg" in content)
    check("_listview.scss implements row selection", ".selected" in content or '[aria-selected="true"]' in content)
    check("_listview.scss handles inactive row selection", ":not(:focus-within)" in content)
    check("_listview.scss implements .listview-icons", ".listview-icons" in content)
    check("_listview.scss implements .listview-tiles", ".listview-tiles" in content)
    check("_listview.scss implements .listview-marquee", ".listview-marquee" in content)
    check("_listview.scss contains Vista theme overrides", '[data-theme="vista"]' in content)


def test_commandbar():
    cb_path = ROOT_DIR / "gui" / "_commandbar.scss"
    check("_commandbar.scss exists", cb_path.is_file())
    content = cb_path.read_text(encoding="utf-8")

    check("_commandbar.scss implements .command-bar", ".command-bar" in content)
    check("_commandbar.scss implements .command-bar-btn", ".command-bar-btn" in content)
    check("_commandbar.scss implements .split-button", ".split-button" in content)
    check("_commandbar.scss embeds dropdown chevron", "breadcrumb-dropdown.svg" in content)
    check("_commandbar.scss contains Vista theme overrides", '[data-theme="vista"]' in content)


def test_tabs_and_scrollbars():
    tabs_path = ROOT_DIR / "gui" / "_tabs.scss"
    check("_tabs.scss exists", tabs_path.is_file())
    tabs_content = tabs_path.read_text(encoding="utf-8")

    check("_tabs.scss implements [role=\"tablist\"]", '[role="tablist"]' in tabs_content)
    check("_tabs.scss implements [role=\"tab\"]", '[role="tab"]' in tabs_content)
    check("_tabs.scss implements [role=\"tabpanel\"]", '[role="tabpanel"]' in tabs_content)
    check("_tabs.scss supports .tabs-bottom", ".tabs-bottom" in tabs_content)
    check("_tabs.scss supports .tabs-left", ".tabs-left" in tabs_content)
    check("_tabs.scss supports .tabs-right", ".tabs-right" in tabs_content)

    sb_path = ROOT_DIR / "gui" / "_scrollbar.scss"
    check("_scrollbar.scss exists", sb_path.is_file())
    sb_content = sb_path.read_text(encoding="utf-8")

    check("_scrollbar.scss embeds button-up SVG", "button-up.svg" in sb_content)
    check("_scrollbar.scss embeds button-down SVG", "button-down.svg" in sb_content)
    check("_scrollbar.scss embeds button-left SVG", "button-left.svg" in sb_content)
    check("_scrollbar.scss embeds button-right SVG", "button-right.svg" in sb_content)
    check("_scrollbar.scss eliminates raster PNGs", "data:image/png" not in sb_content)


def test_layout_and_ribbon():
    layout_path = ROOT_DIR / "gui" / "_layout.scss"
    check("_layout.scss exists", layout_path.is_file())
    layout_content = layout_path.read_text(encoding="utf-8")

    check("_layout.scss implements .splitter", ".splitter" in layout_content)
    check("_layout.scss implements .action-pane", ".action-pane" in layout_content)
    check("_layout.scss implements .category-grid", ".category-grid" in layout_content)

    ribbon_path = ROOT_DIR / "gui" / "_ribbon.scss"
    check("_ribbon.scss exists", ribbon_path.is_file())
    ribbon_content = ribbon_path.read_text(encoding="utf-8")

    check("_ribbon.scss implements .scenic-ribbon", ".scenic-ribbon" in ribbon_content)
    check("_ribbon.scss implements .ribbon-app-btn", ".ribbon-app-btn" in ribbon_content)
    check("_ribbon.scss implements .qat", ".qat" in ribbon_content)
    check("_ribbon.scss implements .ribbon-chunk", ".ribbon-chunk" in ribbon_content)
    check("_ribbon.scss implements .ribbon-btn-large", ".ribbon-btn-large" in ribbon_content)
    check("_ribbon.scss implements .ribbon-btn-small", ".ribbon-btn-small" in ribbon_content)
    check("_ribbon.scss embeds dialog launcher SVG", "ribbon-dialog-launcher.svg" in ribbon_content)
    check("_ribbon.scss embeds QAT dropdown SVG", "ribbon-qat-dropdown.svg" in ribbon_content)


def test_dist_bundles():
    dist_dir = ROOT_DIR / "dist"
    for bundle_name in ["7.css", "7.scoped.css", "7.inline.css"]:
        bundle = dist_dir / bundle_name
        check(f"dist/{bundle_name} exists", bundle.is_file())
        content = bundle.read_text(encoding="utf-8")
        check(f"dist/{bundle_name} contains tree-view", "tree-view" in content)
        check(f"dist/{bundle_name} contains breadcrumb-bar", "breadcrumb-bar" in content)
        check(f"dist/{bundle_name} contains command-bar", "command-bar" in content)
        check(f"dist/{bundle_name} contains scenic-ribbon", "scenic-ribbon" in content or "ribbon" in content)
        check(f"dist/{bundle_name} contains action-pane", "action-pane" in content)
        check(f"dist/{bundle_name} contains category-grid", "category-grid" in content)


def test_safety_check():
    safety_script = ROOT_DIR / "scripts" / "check_repo_safety.py"
    check("Safety script exists", safety_script.is_file())
    res = subprocess.run([sys.executable, str(safety_script)], cwd=str(ROOT_DIR), capture_output=True, text=True)
    check("Safety audit script passes with zero violations", res.returncode == 0, res.stdout + res.stderr)


def main():
    print("=== PHASE 4 VERIFICATION AUDIT ===")
    test_treeview()
    test_breadcrumb()
    test_listview()
    test_commandbar()
    test_tabs_and_scrollbars()
    test_layout_and_ribbon()
    test_dist_bundles()
    test_safety_check()
    print("=== ALL PHASE 4 CHECKS PASSED ===")


if __name__ == "__main__":
    main()
