#!/usr/bin/env python3
"""
scripts/generate_tokens.py

Deterministic compiler that transforms canonical JSON tokens from `assets/tokens/`
into production SCSS stylesheets:
  - gui/_tokens.scss      : Core CSS custom properties and DWM keyframes
  - gui/_aero-tints.scss  : 16-color Aero personalization tints and basic theme fallback
  - gui/_variables.scss   : Aggregator with legacy aliases for backwards compatibility
"""

import json
import os
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_tokens_scss(tokens_dir: Path, output_file: Path):
    colors = load_json(tokens_dir / "colors.json")
    metrics = load_json(tokens_dir / "metrics.json")
    typography = load_json(tokens_dir / "typography.json")
    animations = load_json(tokens_dir / "animations.json")
    aero_math = load_json(tokens_dir / "aero_math.json")
    slices = load_json(tokens_dir / "slices.json")

    lines = []
    lines.append("/* ========================================================================== */")
    lines.append("/* Windows 7 Aero - Core Design Tokens                                      */")
    lines.append("/* Auto-generated from assets/tokens/*.json by scripts/generate_tokens.py    */")
    lines.append("/* DO NOT EDIT DIRECTLY.                                                    */")
    lines.append("/* ========================================================================== */")
    lines.append("")
    lines.append(":root {")

    # Typography
    lines.append("  /* --- Typography & Rendering --- */")
    lines.append(f"  --w7-font-family: {typography['fontFamilies']['primary']};")
    lines.append(f"  --w7-font-family-mono: {typography['fontFamilies']['code']};")
    lines.append(f"  --w7-font-family-script: {typography['fontFamilies']['script']};")
    lines.append(f"  --w7-font-smoothing-webkit: {typography['fontSmoothing']['webkitFontSmoothing']};")
    lines.append(f"  --w7-font-smoothing-moz: {typography['fontSmoothing']['mozOsxFontSmoothing']};")
    lines.append(f"  --w7-font-rendering: {typography['fontSmoothing']['textRendering']};")
    lines.append("  --w7-font: 9pt / 1.35 var(--w7-font-family);")
    lines.append("  --w7-font-size-title: 9pt;")
    lines.append("  --w7-font-size-body: 9pt;")
    lines.append("  --w7-font-size-instruction: 12pt;")
    lines.append("  --w7-font-size-description: 9pt;")
    lines.append("  --w7-font-size-caption: 8pt;")
    lines.append("  --w7-font-weight-normal: 400;")
    lines.append("  --w7-font-weight-semibold: 600;")
    lines.append("  --w7-font-weight-bold: 700;")
    lines.append("")

    # System Colors
    sys_colors = colors.get("system", {})
    lines.append("  /* --- System Colors & Surfaces --- */")
    lines.append(f"  --w7-color-window-bg: {sys_colors.get('windowBg', '#ffffff')};")
    lines.append(f"  --w7-color-window-text: {sys_colors.get('windowText', '#000000')};")
    lines.append(f"  --w7-color-surface: {sys_colors.get('surface', '#f0f0f0')};")
    lines.append(f"  --w7-color-disabled-text: {sys_colors.get('disabledText', '#838383')};")
    lines.append(f"  --w7-color-disabled-border: {sys_colors.get('disabledBorder', '#adb2b5')};")
    lines.append(f"  --w7-color-disabled-bg: {sys_colors.get('disabledBg', '#f4f4f4')};")
    lines.append(f"  --w7-color-highlight-bg: {sys_colors.get('highlightBg', '#3399ff')};")
    lines.append(f"  --w7-color-highlight-text: {sys_colors.get('highlightText', '#ffffff')};")
    lines.append(f"  --w7-color-link: {sys_colors.get('link', '#0066cc')};")
    lines.append(f"  --w7-color-link-hover: {sys_colors.get('linkHover', '#3399ff')};")
    lines.append(f"  --w7-color-title-text: {sys_colors.get('titleText', '#003399')};")
    lines.append(f"  --w7-color-focus-border: {sys_colors.get('focusBorder', '#3d7bad')};")
    lines.append(f"  --w7-color-tooltip-bg: {sys_colors.get('tooltipBg', '#ffffd5')};")
    lines.append(f"  --w7-color-tooltip-border: {sys_colors.get('tooltipBorder', '#767676')};")
    lines.append(f"  --w7-color-tooltip-text: {sys_colors.get('tooltipText', '#000000')};")
    lines.append("")

    # Aero Glass Physics & Shaders
    glass = aero_math.get("glass", {})
    lines.append("  /* --- Aero Glass Optics & Shaders --- */")
    lines.append(f"  --w7-glass-blur: {glass.get('backdropFilter', 'blur(18px) saturate(190%)')};")
    lines.append(f"  --w7-glass-blur-inactive: {glass.get('inactiveBackdropFilter', 'blur(12px) saturate(100%)')};")
    lines.append(f"  --w7-glass-specular-angle: {glass.get('specularGlareAngleDeg', 104)}deg;")
    specular_refs = glass.get("specularReflections", [])
    if len(specular_refs) >= 1:
        lines.append(f"  --w7-glass-specular-reflection: {specular_refs[0]};")
    if len(specular_refs) >= 2:
        lines.append(f"  --w7-glass-glare-reflection: {specular_refs[1]};")
    if len(specular_refs) >= 3:
        lines.append(f"  --w7-glass-depth-gradient: {specular_refs[2]};")
    lines.append(f"  --w7-glass-shadow-restored: {glass.get('boxShadowRestored', 'none')};")
    lines.append(f"  --w7-glass-shadow-inactive: {glass.get('boxShadowInactive', 'none')};")
    lines.append(f"  --w7-glass-shadow-maximized: {glass.get('boxShadowMaximized', 'none')};")
    lines.append(f"  --w7-glass-text-halo-active: {glass.get('textHaloGlowActive', 'none')};")
    lines.append(f"  --w7-glass-text-halo-inactive: {glass.get('textHaloGlowInactive', 'none')};")
    lines.append("  --w7-titlebar-active-text: #000000;")
    lines.append("")

    # Windows Vista Aero Glass & Shaders
    vista_glass = aero_math.get("vistaGlass", {})
    lines.append("  /* --- Windows Vista Aero Glass Optics & Shaders --- */")
    lines.append(f"  --w7-vista-glass-blur: {vista_glass.get('backdropFilter', 'blur(18px) saturate(200%) brightness(85%)')};")
    lines.append(f"  --w7-vista-glass-blur-inactive: {vista_glass.get('inactiveBackdropFilter', 'blur(12px) saturate(110%) brightness(95%)')};")
    lines.append(f"  --w7-vista-glass-specular-angle: {vista_glass.get('specularGlareAngleDeg', 115)}deg;")
    vista_specular = vista_glass.get("specularReflections", [])
    if len(vista_specular) >= 1:
        lines.append(f"  --w7-vista-glass-specular-reflection: {vista_specular[0]};")
    if len(vista_specular) >= 2:
        lines.append(f"  --w7-vista-glass-glare-reflection: {vista_specular[1]};")
    if len(vista_specular) >= 3:
        lines.append(f"  --w7-vista-glass-depth-gradient: {vista_specular[2]};")
    lines.append(f"  --w7-vista-glass-shadow-restored: {vista_glass.get('boxShadowRestored', 'none')};")
    lines.append(f"  --w7-vista-glass-shadow-inactive: {vista_glass.get('boxShadowInactive', 'none')};")
    lines.append(f"  --w7-vista-glass-text-halo-active: {vista_glass.get('textHaloGlowActive', 'none')};")
    lines.append(f"  --w7-vista-glass-text-halo-inactive: {vista_glass.get('textHaloGlowInactive', 'none')};")
    lines.append("  --w7-vista-glass-bg-default: rgba(0, 0, 0, 0.65);")
    lines.append("")

    # Default Aero Tint (Sky Blue)
    default_tint = colors.get("aeroGlass", {}).get("default", {})
    lines.append("  /* --- Default Aero Personalization Tint --- */")
    lines.append(f"  --w7-aero-tint-name: \"default\";")
    lines.append(f"  --w7-aero-tint-color: {default_tint.get('rgba', 'rgba(112, 164, 194, 0.65)')};")
    lines.append(f"  --w7-aero-tint-rgb: 112, 164, 194;")
    lines.append(f"  --w7-aero-tint-hex: {default_tint.get('hex', '#70a4c2')};")
    lines.append("  --w7-aero-border-color: rgba(0, 0, 0, 0.55);")
    lines.append("  --w7-aero-border-inactive: rgba(0, 0, 0, 0.45);")
    lines.append("")

    # Control Primitives: Push Button
    btn = colors.get("controls", {}).get("button", {})
    lines.append("  /* --- Form Controls: Push Button --- */")
    lines.append(f"  --w7-btn-bg: {btn.get('normal', {}).get('background', '')};")
    lines.append(f"  --w7-btn-border: {btn.get('normal', {}).get('border', '')};")
    lines.append("  --w7-btn-border-color: #707070;")
    lines.append(f"  --w7-btn-shadow: {btn.get('normal', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-btn-inner-highlight: {btn.get('normal', {}).get('innerHighlight', '')};")
    lines.append(f"  --w7-btn-hover-bg: {btn.get('hover', {}).get('background', '')};")
    lines.append(f"  --w7-btn-hover-border: {btn.get('hover', {}).get('border', '')};")
    lines.append("  --w7-btn-hover-border-color: #3c7fb1;")
    lines.append(f"  --w7-btn-hover-shadow: {btn.get('hover', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-btn-hover-highlight: {btn.get('hover', {}).get('innerHighlight', '')};")
    lines.append(f"  --w7-btn-pressed-bg: {btn.get('pressed', {}).get('background', '')};")
    lines.append(f"  --w7-btn-pressed-border: {btn.get('pressed', {}).get('border', '')};")
    lines.append("  --w7-btn-pressed-border-color: #2c628b;")
    lines.append(f"  --w7-btn-pressed-shadow: {btn.get('pressed', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-btn-pressed-highlight: {btn.get('pressed', {}).get('innerHighlight', '')};")
    lines.append(f"  --w7-btn-default-bg: {btn.get('default', {}).get('background', 'radial-gradient(circle at bottom, #2aceda, transparent 65%), linear-gradient(#b6d9ee 50%, #1a6ca1 50%)')};")
    lines.append(f"  --w7-btn-default-pulse-bg: {btn.get('defaultPulse', {}).get('background', '')};")
    lines.append(f"  --w7-btn-default-pulse-border: {btn.get('defaultPulse', {}).get('border', '')};")
    lines.append(f"  --w7-btn-default-pulse-glow: {btn.get('defaultPulse', {}).get('outerGlow', '')};")
    lines.append(f"  --w7-btn-disabled-bg: {btn.get('disabled', {}).get('background', '#f4f4f4')};")
    lines.append(f"  --w7-btn-disabled-border: {btn.get('disabled', {}).get('border', '1px solid #adb2b5')};")
    lines.append(f"  --w7-btn-disabled-color: {btn.get('disabled', {}).get('color', '#838383')};")
    lines.append("")

    # Form Controls: Windows Vista Button
    v_btn = colors.get("vistaControls", {}).get("button", {})
    lines.append("  /* --- Form Controls: Windows Vista Button --- */")
    lines.append(f"  --w7-vista-btn-bg: {v_btn.get('normal', {}).get('background', '')};")
    lines.append(f"  --w7-vista-btn-border: {v_btn.get('normal', {}).get('border', '')};")
    lines.append(f"  --w7-vista-btn-hover-bg: {v_btn.get('hover', {}).get('background', '')};")
    lines.append(f"  --w7-vista-btn-hover-border: {v_btn.get('hover', {}).get('border', '')};")
    lines.append(f"  --w7-vista-btn-hover-shadow: {v_btn.get('hover', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-vista-btn-pressed-bg: {v_btn.get('pressed', {}).get('background', '')};")
    lines.append(f"  --w7-vista-btn-pressed-border: {v_btn.get('pressed', {}).get('border', '')};")
    lines.append(f"  --w7-vista-btn-default-pulse-bg: {v_btn.get('defaultPulse', {}).get('background', '')};")
    lines.append("")

    # Command Link
    cmdlink = colors.get("controls", {}).get("commandLink", {})
    lines.append("  /* --- Form Controls: Command Link --- */")
    lines.append(f"  --w7-cmdlink-hover-border: {cmdlink.get('hoverBorder', '1px solid #b8d6fb')};")
    lines.append(f"  --w7-cmdlink-hover-bg: {cmdlink.get('hoverBg', '')};")
    lines.append(f"  --w7-cmdlink-pressed-border: {cmdlink.get('pressedBorder', '1px solid #7da2ce')};")
    lines.append(f"  --w7-cmdlink-pressed-bg: {cmdlink.get('pressedBg', '')};")
    lines.append("")

    # Text Input
    inp = colors.get("controls", {}).get("input", {})
    lines.append("  /* --- Form Controls: Input --- */")
    lines.append(f"  --w7-input-border: {inp.get('border', '1px solid #8e8f8f')};")
    lines.append(f"  --w7-input-border-hover: {inp.get('borderHover', '1px solid #5c5d5d')};")
    lines.append(f"  --w7-input-border-focus: {inp.get('borderFocus', '1px solid #3d7bad')};")
    lines.append(f"  --w7-input-bg: {inp.get('bg', '#ffffff')};")
    lines.append(f"  --w7-input-bg-disabled: {inp.get('bgDisabled', '#f4f4f4')};")
    lines.append("")

    # Checkbox
    cb = colors.get("controls", {}).get("checkbox", {})
    lines.append("  /* --- Form Controls: Checkbox --- */")
    lines.append(f"  --w7-checkbox-bg: {cb.get('normal', {}).get('background', '')};")
    lines.append(f"  --w7-checkbox-border: {cb.get('normal', {}).get('border', '')};")
    lines.append(f"  --w7-checkbox-shadow: {cb.get('normal', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-checkbox-hover-bg: {cb.get('hover', {}).get('background', '')};")
    lines.append(f"  --w7-checkbox-hover-border: {cb.get('hover', {}).get('border', '')};")
    lines.append(f"  --w7-checkbox-hover-shadow: {cb.get('hover', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-checkbox-pressed-bg: {cb.get('pressed', {}).get('background', '')};")
    lines.append(f"  --w7-checkbox-pressed-border: {cb.get('pressed', {}).get('border', '')};")
    lines.append(f"  --w7-checkbox-pressed-shadow: {cb.get('pressed', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-checkbox-disabled-bg: {cb.get('disabled', {}).get('background', '#f4f4f4')};")
    lines.append(f"  --w7-checkbox-disabled-border: {cb.get('disabled', {}).get('border', '1px solid #adb2b5')};")
    lines.append(f"  --w7-checkbox-glyph-color: {cb.get('glyphColor', '#1e395b')};")
    lines.append(f"  --w7-checkbox-disabled-glyph-color: {cb.get('disabled', {}).get('glyphColor', '#838383')};")
    lines.append("")

    # Radio
    rad = colors.get("controls", {}).get("radio", {})
    lines.append("  /* --- Form Controls: Radio Button --- */")
    lines.append(f"  --w7-radio-bg: {rad.get('normal', {}).get('background', '')};")
    lines.append(f"  --w7-radio-border: {rad.get('normal', {}).get('border', '')};")
    lines.append(f"  --w7-radio-shadow: {rad.get('normal', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-radio-hover-bg: {rad.get('hover', {}).get('background', '')};")
    lines.append(f"  --w7-radio-hover-border: {rad.get('hover', {}).get('border', '')};")
    lines.append(f"  --w7-radio-hover-shadow: {rad.get('hover', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-radio-pressed-bg: {rad.get('pressed', {}).get('background', '')};")
    lines.append(f"  --w7-radio-pressed-border: {rad.get('pressed', {}).get('border', '')};")
    lines.append(f"  --w7-radio-pressed-shadow: {rad.get('pressed', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-radio-disabled-bg: {rad.get('disabled', {}).get('background', '#f4f4f4')};")
    lines.append(f"  --w7-radio-disabled-border: {rad.get('disabled', {}).get('border', '1px solid #adb2b5')};")
    lines.append(f"  --w7-radio-bullet-color: {rad.get('bullet', {}).get('color', '#1e395b')};")
    lines.append(f"  --w7-radio-bullet-gradient: {rad.get('bullet', {}).get('gradient', '')};")
    lines.append(f"  --w7-radio-disabled-bullet-color: {rad.get('disabled', {}).get('bulletColor', '#838383')};")
    lines.append("")

    # Slider
    slider = colors.get("controls", {}).get("slider", {})
    lines.append("  /* --- Form Controls: Slider / Trackbar --- */")
    lines.append(f"  --w7-slider-track-bg: {slider.get('track', {}).get('background', '#d9d9d9')};")
    lines.append(f"  --w7-slider-track-border: {slider.get('track', {}).get('border', '1px solid #9c9c9c')};")
    lines.append(f"  --w7-slider-track-shadow: {slider.get('track', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-slider-thumb-bg: {slider.get('thumb', {}).get('normal', {}).get('background', '')};")
    lines.append(f"  --w7-slider-thumb-border: {slider.get('thumb', {}).get('normal', {}).get('border', '')};")
    lines.append(f"  --w7-slider-thumb-shadow: {slider.get('thumb', {}).get('normal', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-slider-thumb-hover-bg: {slider.get('thumb', {}).get('hover', {}).get('background', '')};")
    lines.append(f"  --w7-slider-thumb-hover-border: {slider.get('thumb', {}).get('hover', {}).get('border', '')};")
    lines.append(f"  --w7-slider-thumb-hover-shadow: {slider.get('thumb', {}).get('hover', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-slider-thumb-pressed-bg: {slider.get('thumb', {}).get('pressed', {}).get('background', '')};")
    lines.append(f"  --w7-slider-thumb-pressed-border: {slider.get('thumb', {}).get('pressed', {}).get('border', '')};")
    lines.append(f"  --w7-slider-thumb-pressed-shadow: {slider.get('thumb', {}).get('pressed', {}).get('boxShadow', '')};")
    lines.append(f"  --w7-slider-tick-color: {slider.get('tickColor', '#9c9c9c')};")
    lines.append("")

    # Spinner
    sp = colors.get("controls", {}).get("spinner", {})
    lines.append("  /* --- Form Controls: Spin Button --- */")
    lines.append(f"  --w7-spinner-btn-bg: {sp.get('normal', {}).get('background', '')};")
    lines.append(f"  --w7-spinner-btn-border: {sp.get('normal', {}).get('border', '')};")
    lines.append(f"  --w7-spinner-btn-hover-bg: {sp.get('hover', {}).get('background', '')};")
    lines.append(f"  --w7-spinner-btn-hover-border: {sp.get('hover', {}).get('border', '')};")
    lines.append(f"  --w7-spinner-btn-pressed-bg: {sp.get('pressed', {}).get('background', '')};")
    lines.append(f"  --w7-spinner-btn-pressed-border: {sp.get('pressed', {}).get('border', '')};")
    lines.append(f"  --w7-spinner-arrow-color: {sp.get('arrowColor', '#333333')};")
    lines.append(f"  --w7-spinner-arrow-hover-color: {sp.get('arrowColorHover', '#1e395b')};")
    lines.append(f"  --w7-spinner-arrow-disabled-color: {sp.get('arrowColorDisabled', '#838383')};")
    lines.append("")

    # Groupbox
    gb = colors.get("controls", {}).get("groupbox", {})
    lines.append("  /* --- Form Controls: Group Box --- */")
    lines.append(f"  --w7-groupbox-border: {gb.get('border', '1px solid #d9d9d9')};")
    lines.append(f"  --w7-groupbox-highlight: {gb.get('highlight', 'inset 0 1px 0 #ffffff')};")
    lines.append(f"  --w7-groupbox-legend-color: {gb.get('legendColor', '#003399')};")
    lines.append("")

    # Combobox & Dropdown
    combo = colors.get("controls", {}).get("combobox", {})
    lines.append("  /* --- Form Controls: Combobox & Dropdown --- */")
    lines.append(f"  --w7-combobox-btn-bg: {combo.get('buttonBg', '')};")
    lines.append(f"  --w7-combobox-btn-border: {combo.get('buttonBorder', '1px solid #707070')};")
    lines.append(f"  --w7-combobox-btn-hover-bg: {combo.get('buttonHoverBg', '')};")
    lines.append(f"  --w7-combobox-btn-hover-border: {combo.get('buttonHoverBorder', '1px solid #3c7fb1')};")
    lines.append(f"  --w7-combobox-btn-pressed-bg: {combo.get('buttonPressedBg', '')};")
    lines.append(f"  --w7-combobox-btn-pressed-border: {combo.get('buttonPressedBorder', '1px solid #2c628b')};")
    v_combo = colors.get("vistaControls", {}).get("combobox", {})
    lines.append(f"  --w7-vista-combobox-btn-bg: {v_combo.get('buttonBg', '')};")
    lines.append(f"  --w7-vista-combobox-btn-hover-bg: {v_combo.get('buttonHoverBg', '')};")
    lines.append(f"  --w7-vista-combobox-btn-hover-glow: {v_combo.get('hoverGlow', '')};")
    lines.append("")

    # Listbox
    lb = colors.get("controls", {}).get("listbox", {})
    lines.append("  /* --- Form Controls: Listbox --- */")
    lines.append(f"  --w7-listbox-border: {lb.get('border', '1px solid #8e8f8f')};")
    lines.append(f"  --w7-listbox-bg: {lb.get('bg', '#ffffff')};")
    lines.append(f"  --w7-listbox-selected-bg: {lb.get('selectedBg', '')};")
    lines.append(f"  --w7-listbox-selected-border: {lb.get('selectedBorder', '1px solid #84acdd')};")
    lines.append(f"  --w7-listbox-hover-bg: {lb.get('hoverBg', '')};")
    lines.append(f"  --w7-listbox-hover-border: {lb.get('hoverBorder', '1px solid #e5f3fb')};")
    lines.append("")

    # Progress Bars
    prog = colors.get("progress", {})
    lines.append("  /* --- Progress Bar --- */")
    lines.append(f"  --w7-progress-normal-chunk: {prog.get('normal', {}).get('chunk', '')};")
    lines.append(f"  --w7-progress-normal-border: {prog.get('normal', {}).get('chunkBorder', '')};")
    lines.append(f"  --w7-progress-normal-track: {prog.get('normal', {}).get('track', '')};")
    lines.append(f"  --w7-progress-paused-chunk: {prog.get('paused', {}).get('chunk', '')};")
    lines.append(f"  --w7-progress-paused-border: {prog.get('paused', {}).get('chunkBorder', '')};")
    lines.append(f"  --w7-progress-error-chunk: {prog.get('error', {}).get('chunk', '')};")
    lines.append(f"  --w7-progress-error-border: {prog.get('error', {}).get('chunkBorder', '')};")
    lines.append("")

    # UAC Banners
    uac = colors.get("uacBanners", {})
    lines.append("  /* --- UAC Banners --- */")
    lines.append(f"  --w7-uac-admin-bg: {uac.get('administrativeSigned', {}).get('gradient', '')};")
    lines.append(f"  --w7-uac-warning-bg: {uac.get('unknownPublisher', {}).get('gradient', '')};")
    lines.append(f"  --w7-uac-blocked-bg: {uac.get('blockedRestricted', {}).get('gradient', '')};")
    lines.append("")

    # Windows Basic
    basic = colors.get("windowsBasic", {})
    lines.append("  /* --- Windows Basic Theme --- */")
    lines.append(f"  --w7-basic-title-active-bg: {basic.get('titleBarActive', {}).get('gradient', '')};")
    lines.append(f"  --w7-basic-title-active-border: {basic.get('titleBarActive', {}).get('border', '')};")
    lines.append(f"  --w7-basic-title-inactive-bg: {basic.get('titleBarInactive', {}).get('gradient', '')};")
    lines.append(f"  --w7-basic-title-inactive-border: {basic.get('titleBarInactive', {}).get('border', '')};")
    lines.append(f"  --w7-basic-frame-border: {basic.get('frameBorder', '')};")
    lines.append(f"  --w7-basic-high-contrast-border: {basic.get('highContrastBorder', '2px solid #000000')};")
    lines.append("")

    # Windows Vista Basic
    v_basic = colors.get("vistaBasic", {})
    lines.append("  /* --- Windows Vista Basic Theme --- */")
    lines.append(f"  --w7-vista-basic-title-active-bg: {v_basic.get('titleBarActive', {}).get('gradient', '')};")
    lines.append(f"  --w7-vista-basic-title-active-border: {v_basic.get('titleBarActive', {}).get('border', '')};")
    lines.append(f"  --w7-vista-basic-title-inactive-bg: {v_basic.get('titleBarInactive', {}).get('gradient', '')};")
    lines.append(f"  --w7-vista-basic-title-inactive-border: {v_basic.get('titleBarInactive', {}).get('border', '')};")
    lines.append(f"  --w7-vista-basic-frame-border: {v_basic.get('frameBorder', '')};")
    lines.append("")

    # Task Dialog
    td = colors.get("taskDialog", {})
    lines.append("  /* --- Task Dialog --- */")
    lines.append(f"  --w7-dialog-instruction-color: {td.get('instructionColor', '#003399')};")
    lines.append(f"  --w7-dialog-footer-bg: {td.get('footerBackground', '#f0f0f0')};")
    lines.append(f"  --w7-dialog-footer-border: {td.get('footerBorder', '1px solid #dfdfdf')};")
    lines.append("")

    # Ribbon
    ribbon = colors.get("ribbon", {})
    lines.append("  /* --- Ribbon System --- */")
    lines.append(f"  --w7-ribbon-bg: {ribbon.get('background', '')};")
    lines.append(f"  --w7-ribbon-border: {ribbon.get('border', '')};")
    lines.append(f"  --w7-ribbon-tab-active-bg: {ribbon.get('tabActiveBackground', '#ffffff')};")
    lines.append(f"  --w7-ribbon-tab-active-border: {ribbon.get('tabActiveBorder', '')};")
    lines.append(f"  --w7-ribbon-tab-hover-bg: {ribbon.get('tabHoverGradient', '')};")
    lines.append(f"  --w7-ribbon-app-btn-wordpad: {ribbon.get('appButtonWordpad', '')};")
    lines.append(f"  --w7-ribbon-app-btn-paint: {ribbon.get('appButtonPaint', '')};")
    lines.append(f"  --w7-ribbon-chunk-border: {ribbon.get('chunkBorder', '')};")
    lines.append(f"  --w7-ribbon-chunk-hover-border: {ribbon.get('chunkHoverBorder', '')};")
    lines.append(f"  --w7-ribbon-ruler-bg: {ribbon.get('rulerBackground', '#fbfbfc')};")
    lines.append(f"  --w7-ribbon-ruler-border: {ribbon.get('rulerBorder', '')};")
    lines.append(f"  --w7-ribbon-ruler-tick: {ribbon.get('rulerTickColor', '#828790')};")
    lines.append("")

    # Metrics
    win_m = metrics.get("windows", {})
    cap_m = win_m.get("captionButton", {})
    ctrl_m = metrics.get("controls", {})
    lines.append("  /* --- Metrics & Dimensions --- */")
    lines.append(f"  --w7-metric-window-border-width: {win_m.get('windowBorderThicknessPx', 6)}px;")
    lines.append(f"  --w7-metric-window-radius: {win_m.get('windowBorderRadiusRestoredPx', 6)}px;")
    lines.append(f"  --w7-metric-window-radius-maximized: {win_m.get('windowBorderRadiusMaximizedPx', 0)}px;")
    lines.append(f"  --w7-metric-titlebar-height: {win_m.get('titleBarHeightRestoredPx', 30)}px;")
    lines.append(f"  --w7-metric-titlebar-height-maximized: {win_m.get('titleBarHeightMaximizedPx', 22)}px;")
    lines.append(f"  --w7-metric-caption-btn-width: {cap_m.get('widthPx', 45)}px;")
    lines.append(f"  --w7-metric-caption-btn-height: {cap_m.get('heightPx', 20)}px;")
    lines.append(f"  --w7-metric-caption-close-width: {cap_m.get('closeWidthPx', 47)}px;")
    lines.append(f"  --w7-metric-caption-margin-right: {cap_m.get('marginRightPx', 2)}px;")
    lines.append(f"  --w7-metric-btn-min-width: {ctrl_m.get('button', {}).get('minWidthPx', 75)}px;")
    lines.append(f"  --w7-metric-btn-height: {ctrl_m.get('button', {}).get('heightPx', 23)}px;")
    lines.append(f"  --w7-metric-btn-radius: {ctrl_m.get('button', {}).get('borderRadiusPx', 3)}px;")
    lines.append(f"  --w7-metric-btn-padding: {ctrl_m.get('button', {}).get('paddingPx', '0 12px')};")
    lines.append(f"  --w7-metric-input-height: {ctrl_m.get('input', {}).get('heightPx', 21)}px;")
    lines.append(f"  --w7-metric-input-radius: {ctrl_m.get('input', {}).get('borderRadiusPx', 2)}px;")
    lines.append(f"  --w7-metric-input-padding: {ctrl_m.get('input', {}).get('paddingPx', '2px 5px')};")
    lines.append(f"  --w7-metric-checkbox-size: {ctrl_m.get('checkbox', {}).get('sizePx', 13)}px;")
    lines.append(f"  --w7-metric-radio-size: {ctrl_m.get('radio', {}).get('sizePx', 13)}px;")
    lines.append(f"  --w7-metric-command-link-glyph: {ctrl_m.get('commandLink', {}).get('glyphSizePx', 24)}px;")
    lines.append(f"  --w7-metric-slider-track-height: {ctrl_m.get('slider', {}).get('trackHeightPx', 4)}px;")
    lines.append(f"  --w7-metric-slider-thumb-width: {ctrl_m.get('slider', {}).get('thumbWidthPx', 11)}px;")
    lines.append(f"  --w7-metric-slider-thumb-height: {ctrl_m.get('slider', {}).get('thumbHeightPx', 21)}px;")
    lines.append(f"  --w7-metric-spinner-width: {ctrl_m.get('spinner', {}).get('widthPx', 16)}px;")
    lines.append(f"  --w7-metric-groupbox-radius: {ctrl_m.get('groupbox', {}).get('borderRadiusPx', 3)}px;")
    lines.append(f"  --w7-metric-groupbox-padding: {ctrl_m.get('groupbox', {}).get('paddingPx', '10px')};")
    combo_m = ctrl_m.get("combobox", {})
    lines.append(f"  --w7-metric-combobox-btn-width: {combo_m.get('buttonWidthPx', 17)}px;")
    lines.append(f"  --w7-metric-combobox-height: {combo_m.get('heightPx', 23)}px;")
    lines.append(f"  --w7-metric-combobox-radius: {combo_m.get('borderRadiusPx', 3)}px;")
    lines.append("  --w7-metric-scrollbar-width: 17px;")
    lines.append(f"  --w7-metric-ribbon-height: {metrics.get('ribbon', {}).get('heightPx', 92)}px;")
    lines.append(f"  --w7-metric-ribbon-tab-height: {metrics.get('ribbon', {}).get('tabHeightPx', 24)}px;")
    lines.append(f"  --w7-metric-taskbar-height: {metrics.get('taskbar', {}).get('heightPx', 40)}px;")
    lines.append("")

    # Windows Vista Metrics
    v_win_m = metrics.get("vistaWindows", {})
    v_cap_m = v_win_m.get("captionButton", {})
    lines.append("  /* --- Windows Vista Metrics --- */")
    lines.append(f"  --w7-vista-metric-window-border-width: {v_win_m.get('windowBorderThicknessPx', 7)}px;")
    lines.append(f"  --w7-vista-metric-window-radius: {v_win_m.get('windowBorderRadiusRestoredPx', 8)}px;")
    lines.append(f"  --w7-vista-metric-window-radius-maximized: {v_win_m.get('windowBorderRadiusMaximizedPx', 0)}px;")
    lines.append(f"  --w7-vista-metric-titlebar-height: {v_win_m.get('titleBarHeightRestoredPx', 30)}px;")
    lines.append(f"  --w7-vista-metric-titlebar-height-maximized: {v_win_m.get('titleBarHeightMaximizedPx', 26)}px;")
    lines.append(f"  --w7-vista-metric-caption-btn-width: {v_cap_m.get('widthPx', 43)}px;")
    lines.append(f"  --w7-vista-metric-caption-btn-height: {v_cap_m.get('heightPx', 19)}px;")
    lines.append(f"  --w7-vista-metric-caption-close-width: {v_cap_m.get('closeWidthPx', 45)}px;")
    lines.append(f"  --w7-vista-metric-caption-margin-right: {v_cap_m.get('marginRightPx', 2)}px;")
    lines.append("")

    # Animations & Timing
    curves = animations.get("curves", {})
    durations = animations.get("durations", {})
    lines.append("  /* --- DWM Animation Timing & Easing Curves --- */")
    lines.append(f"  --w7-ease-fast-entrance: {curves.get('fastEntrance', 'cubic-bezier(0.0, 0.0, 0.2, 1.0)')};")
    lines.append(f"  --w7-ease-sinusoidal-pulse: {curves.get('sinusoidalPulse', 'cubic-bezier(0.45, 0.05, 0.55, 0.95)')};")
    lines.append(f"  --w7-ease-phosphorescent-decay: {curves.get('phosphorescentDecay', 'cubic-bezier(0.2, 0.8, 0.2, 1.0)')};")
    lines.append(f"  --w7-ease-disclosure: {curves.get('disclosureExpand', 'cubic-bezier(0.1, 0.9, 0.2, 1.0)')};")
    lines.append(f"  --w7-dur-btn-pulse: {durations.get('defaultButtonPulse', '1100ms')};")
    lines.append(f"  --w7-dur-btn-hover-in: {durations.get('buttonHoverEntrance', '120ms')};")
    lines.append(f"  --w7-dur-btn-hover-out: {durations.get('buttonHoverDecay', '750ms')};")
    lines.append(f"  --w7-dur-progress-shimmer: {durations.get('progressShimmerCycle', '3000ms')};")
    lines.append(f"  --w7-dur-progress-indeterminate: {durations.get('progressIndeterminateCycle', '2000ms')};")
    lines.append(f"  --w7-dur-window-morph: {durations.get('windowDwmMorph', '250ms')};")
    lines.append(f"  --w7-dur-tooltip-delay: {durations.get('tooltipDelay', '400ms')};")
    lines.append(f"  --w7-dur-disclosure: {durations.get('taskDialogDisclosure', '200ms')};")
    lines.append("}")
    lines.append("")

    # Keyframes
    lines.append("/* --- DWM Hardware-Accelerated Keyframe Sequences --- */")
    lines.append("@keyframes w7-aero-button-pulse {")
    lines.append("  0%, 100% {")
    lines.append("    border-color: #5586a3;")
    lines.append("    box-shadow: inset 0 0 3px 1px rgba(52, 222, 255, 0.85), 0 0 2px rgba(52, 222, 255, 0.5);")
    lines.append("  }")
    lines.append("  50% {")
    lines.append("    border-color: #2c688d;")
    lines.append("    box-shadow: inset 0 0 6px 2px rgba(52, 222, 255, 1.0), 0 0 8px rgba(52, 222, 255, 0.85);")
    lines.append("  }")
    lines.append("}")
    lines.append("")
    lines.append("@keyframes w7-vista-button-pulse {")
    lines.append("  0%, 100% {")
    lines.append("    border-color: #3c7fb1;")
    lines.append("    box-shadow: 0 0 3px rgba(0, 160, 240, 0.4), inset 0 0 2px rgba(255, 255, 255, 0.6);")
    lines.append("  }")
    lines.append("  50% {")
    lines.append("    border-color: #1c6ba0;")
    lines.append("    box-shadow: 0 0 8px rgba(0, 160, 240, 0.85), inset 0 0 4px rgba(255, 255, 255, 0.9);")
    lines.append("  }")
    lines.append("}")
    lines.append("")
    lines.append("@keyframes w7-progress-shimmer {")
    lines.append("  0% { transform: translateX(-100%); }")
    lines.append("  100% { transform: translateX(200%); }")
    lines.append("}")
    lines.append("")
    lines.append("@keyframes w7-caption-glow {")
    lines.append("  0% { opacity: 0; }")
    lines.append("  100% { opacity: 1; }")
    lines.append("}")
    lines.append("")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_aero_tints_scss(tokens_dir: Path, output_file: Path):
    colors = load_json(tokens_dir / "colors.json")
    aero_tints = colors.get("aeroGlass", {})
    basic = colors.get("windowsBasic", {})

    lines = []
    lines.append("/* ========================================================================== */")
    lines.append("/* Windows 7 Aero - 16-Color Personalization Engine                          */")
    lines.append("/* Auto-generated from assets/tokens/colors.json by scripts/generate_tokens.py */")
    lines.append("/* ========================================================================== */")
    lines.append("")

    # Map each tint to RGB tuple and styling rules
    rgb_map = {
        "pumpkin": "196, 105, 49",
        "violet": "111, 78, 184",
        "frost": "229, 236, 240",
        "lime": "143, 168, 59",
        "sea": "65, 125, 138",
        "blush": "184, 89, 124",
        "ruby": "184, 62, 62",
        "sun": "201, 155, 59",
        "leaf": "94, 139, 78",
        "slate": "91, 108, 122",
        "fuchsia": "168, 59, 139",
        "default": "112, 164, 194",
        "smoke": "71, 71, 71",
        "sky": "87, 139, 184",
        "pink": "196, 101, 155",
        "twilight": "69, 82, 99",
    }

    for tint_key, tint_data in aero_tints.items():
        name = tint_data.get("name", tint_key.capitalize())
        rgba = tint_data.get("rgba", "")
        hex_val = tint_data.get("hex", "")
        rgb_tuple = rgb_map.get(tint_key, "112, 164, 194")

        lines.append(f"/* Aero Tint: {name} */")
        lines.append(f"[data-aero-tint=\"{tint_key}\"],")
        lines.append(f".window[data-aero-tint=\"{tint_key}\"] {{")
        lines.append(f"  --w7-aero-tint-name: \"{tint_key}\";")
        lines.append(f"  --w7-aero-tint-color: {rgba};")
        lines.append(f"  --w7-aero-tint-rgb: {rgb_tuple};")
        lines.append(f"  --w7-aero-tint-hex: {hex_val};")
        lines.append(f"  --w7-w-bg: {rgba};")
        lines.append(f"  --w7-w-grad: linear-gradient(to right, rgba(255, 255, 255, 0.4), rgba(0, 0, 0, 0.1), rgba(255, 255, 255, 0.2)), {rgba};")
        lines.append("}")
        lines.append("")

    # Basic Theme Fallback
    lines.append("/* Windows Basic Theme (Non-Composited DWM Fallback) */")
    lines.append("[data-theme=\"basic\"],")
    lines.append(".window[data-theme=\"basic\"] {")
    lines.append("  --w7-glass-blur: none;")
    lines.append("  --w7-glass-specular-reflection: none;")
    lines.append("  --w7-glass-glare-reflection: none;")
    lines.append("  --w7-glass-depth-gradient: none;")
    lines.append(f"  --w7-w-bg: #99b4d1;")
    lines.append(f"  --w7-w-grad: {basic.get('titleBarActive', {}).get('gradient', 'linear-gradient(to bottom, #99b4d1 0%, #b9d1ea 100%)')};")
    lines.append(f"  --w7-w-bd: #7592b2;")
    lines.append("}")
    lines.append("")

    # High Contrast Fallback
    lines.append("/* Windows High Contrast Theme */")
    lines.append("[data-theme=\"high-contrast\"],")
    lines.append(".window[data-theme=\"high-contrast\"] {")
    lines.append("  --w7-glass-blur: none;")
    lines.append("  --w7-w-bg: #000000;")
    lines.append("  --w7-w-grad: #000000;")
    lines.append("  --w7-w-bd: #ffffff;")
    lines.append("  --w7-color-window-bg: #000000;")
    lines.append("  --w7-color-window-text: #ffffff;")
    lines.append("}")
    lines.append("")

    # Windows Vista Theming & 8 Canonical Personalization Tints
    lines.append("/* ========================================================================== */")
    lines.append("/* Windows Vista Aero Theming & Canonical Personalization Tints             */")
    lines.append("/* ========================================================================== */")
    lines.append("")
    lines.append("/* Windows Vista Aero Base (Default Charcoal / Black Glass) */")
    lines.append("[data-theme=\"vista\"],")
    lines.append(".window[data-theme=\"vista\"] {")
    lines.append("  --w7-aero-tint-name: \"graphite\";")
    lines.append("  --w7-aero-tint-color: rgba(0, 0, 0, 0.65);")
    lines.append("  --w7-aero-tint-rgb: 0, 0, 0;")
    lines.append("  --w7-aero-tint-hex: #000000;")
    lines.append("  --w7-w-bg: rgba(0, 0, 0, 0.65);")
    lines.append("  --w7-w-grad: var(--w7-vista-glass-specular-reflection), rgba(0, 0, 0, 0.65);")
    lines.append("  --w7-glass-specular-reflection: var(--w7-vista-glass-specular-reflection);")
    lines.append("  --w7-glass-text-halo-active: var(--w7-vista-glass-text-halo-active);")
    lines.append("  --w7-glass-text-halo-inactive: var(--w7-vista-glass-text-halo-inactive);")
    lines.append("  --w7-glass-shadow-restored: var(--w7-vista-glass-shadow-restored);")
    lines.append("  --w7-glass-shadow-inactive: var(--w7-vista-glass-shadow-inactive);")
    lines.append("}")
    lines.append("")

    vista_tints = colors.get("vistaAeroGlass", {})
    vista_rgb_map = {
        "default": "0, 0, 0",
        "graphite": "0, 0, 0",
        "teal": "46, 111, 126",
        "red": "139, 29, 29",
        "yellow": "158, 129, 30",
        "green": "39, 106, 38",
        "orange": "154, 78, 30",
        "pink": "137, 45, 99",
        "frost": "205, 216, 224",
    }

    for tint_key, tint_data in vista_tints.items():
        name = tint_data.get("name", tint_key.capitalize())
        rgba = tint_data.get("rgba", "")
        hex_val = tint_data.get("hex", "")
        rgb_tuple = vista_rgb_map.get(tint_key, "0, 0, 0")

        lines.append(f"/* Vista Aero Tint: {name} */")
        lines.append(f"[data-theme=\"vista\"][data-aero-tint=\"{tint_key}\"],")
        lines.append(f".window[data-theme=\"vista\"][data-aero-tint=\"{tint_key}\"] {{")
        lines.append(f"  --w7-aero-tint-name: \"{tint_key}\";")
        lines.append(f"  --w7-aero-tint-color: {rgba};")
        lines.append(f"  --w7-aero-tint-rgb: {rgb_tuple};")
        lines.append(f"  --w7-aero-tint-hex: {hex_val};")
        lines.append(f"  --w7-w-bg: {rgba};")
        lines.append(f"  --w7-w-grad: var(--w7-vista-glass-specular-reflection), {rgba};")
        lines.append("}")
        lines.append("")

    # Maximized Vista Window (Solid Opaque Black Frame)
    lines.append("/* Maximized Vista Window (Solid Opaque Black Frame - Authentic Vista DWM Behavior) */")
    lines.append("[data-theme=\"vista\"].maximized,")
    lines.append(".window.maximized[data-theme=\"vista\"],")
    lines.append("[data-theme=\"vista\"] .window.maximized {")
    lines.append("  --w7-glass-blur: none;")
    lines.append("  --w7-w-bg: #000000;")
    lines.append("  --w7-w-grad: #000000;")
    lines.append("  --w7-w-bd: #000000;")
    lines.append("  background: #000000;")
    lines.append("}")
    lines.append("")

    # Windows Vista Basic Theme Fallback
    vista_basic = colors.get("vistaBasic", {})
    lines.append("/* Windows Vista Basic Theme (Non-Composited DWM Fallback) */")
    lines.append("[data-theme=\"vista-basic\"],")
    lines.append(".window[data-theme=\"vista-basic\"] {")
    lines.append("  --w7-glass-blur: none;")
    lines.append("  --w7-glass-specular-reflection: none;")
    lines.append("  --w7-glass-glare-reflection: none;")
    lines.append("  --w7-glass-depth-gradient: none;")
    lines.append("  --w7-w-bg: #4c6b8c;")
    lines.append(f"  --w7-w-grad: {vista_basic.get('titleBarActive', {}).get('gradient', 'linear-gradient(to bottom, #4c6b8c 0%, #364f6b 50%, #2b3f56 51%, #354e6a 100%)')};")
    lines.append(f"  --w7-w-bd: {vista_basic.get('frameBorder', '4px solid #364f6b')};")
    lines.append("  --w7-color-window-text: #ffffff;")
    lines.append("  --w7-titlebar-active-text: #ffffff;")
    lines.append("}")
    lines.append("")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def generate_variables_scss(output_file: Path):
    lines = []
    lines.append("/* ========================================================================== */")
    lines.append("/* Windows 7 Aero - Primary Variables & Backward Compatibility Mapping       */")
    lines.append("/* Auto-generated by scripts/generate_tokens.py.                             */")
    lines.append("/* ========================================================================== */")
    lines.append("")
    lines.append("@import \"_tokens.scss\";")
    lines.append("@import \"_aero-tints.scss\";")
    lines.append("")
    lines.append(":root {")
    lines.append("  /* --- Legacy Variable Aliases for Unrefactored Components --- */")
    lines.append("  --w7-font: 9pt / 1.35 var(--w7-font-family);")
    lines.append("  --w7-surface: var(--w7-color-surface);")
    lines.append("")
    lines.append("  --w7-el-bg: #f2f2f2;")
    lines.append("  --w7-el-bg-d: var(--w7-btn-disabled-bg);")
    lines.append("  --w7-el-bg-s-1: #ebebeb;")
    lines.append("  --w7-el-bg-s-2: #cfcfcf;")
    lines.append("")
    lines.append("  --w7-el-sd: var(--w7-btn-shadow);")
    lines.append("  --w7-el-sd-a: var(--w7-btn-pressed-shadow);")
    lines.append("")
    lines.append("  --w7-el-bd: var(--w7-btn-border-color);")
    lines.append("  --w7-el-bd-h: var(--w7-btn-hover-border-color);")
    lines.append("  --w7-el-bd-a: var(--w7-btn-pressed-border-color);")
    lines.append("  --w7-el-bd-d: var(--w7-btn-disabled-border);")
    lines.append("  --w7-el-bdr: var(--w7-metric-btn-radius);")
    lines.append("")
    lines.append("  --w7-el-c: var(--w7-color-window-text);")
    lines.append("  --w7-el-c-d: var(--w7-color-disabled-text);")
    lines.append("")
    lines.append("  --w7-el-grad: var(--w7-btn-bg);")
    lines.append("  --w7-el-grad-h: var(--w7-btn-hover-bg);")
    lines.append("  --w7-el-grad-a: var(--w7-btn-pressed-bg);")
    lines.append("")
    lines.append("  --w7-li-bd-hl: #aaddfa;")
    lines.append("  --w7-li-bg-hl: linear-gradient(#fff9, #e6ecf5cc 90%, #fffc);")
    lines.append("}")
    lines.append("")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    root_dir = Path(__file__).resolve().parent.parent
    tokens_dir = root_dir / "assets" / "tokens"
    gui_dir = root_dir / "gui"

    print("Generating SCSS tokens from JSON sources...")
    generate_tokens_scss(tokens_dir, gui_dir / "_tokens.scss")
    print(f"  -> Generated {gui_dir / '_tokens.scss'}")

    generate_aero_tints_scss(tokens_dir, gui_dir / "_aero-tints.scss")
    print(f"  -> Generated {gui_dir / '_aero-tints.scss'}")

    generate_variables_scss(gui_dir / "_variables.scss")
    print(f"  -> Generated {gui_dir / '_variables.scss'}")

    print("Tokens generation complete.")


if __name__ == "__main__":
    main()
