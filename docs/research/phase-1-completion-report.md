# Phase 1 Token Architecture & Color Engine Audit Report

This report documents the architectural design, compilation pipeline, token coverage, and verification results for Phase 1 of the `7.css` restoration.

---

## 1. Executive Summary & Objective

Phase 1 established the design token architecture, Aero personalization engine, and typographic foundations for `7.css`. The primary objective was replacing hardcoded, fragmented CSS declarations with a centralized token dictionary compiled directly from canonical JSON schemas.

The token system bridges authentic Windows 7 Aero styling with modern CSS custom properties (`--w7-*`). It provides the color stops, DWM physics constants, dimensional metrics, and typography scales required for upcoming component rebuilds in Phase 2 through Phase 5.

---

## 2. Token Compiler Architecture

To eliminate schema drift between design specifications and runtime stylesheets, token generation is fully automated via `scripts/generate_tokens.py`.

### Canonical Sources (`assets/tokens/`)
The compiler consumes six structured JSON schemas:
1. `colors.json`: System colors, 16 Aero tints, basic theme palette, form control states, progress bar gradients, and UAC banner levels.
2. `metrics.json`: Win32 DLU formulas, window borders, title bar heights, caption button hitboxes, and control dimensions.
3. `typography.json`: Segoe UI type scale, font weights, line heights, and subpixel font smoothing declarations.
4. `animations.json`: DWM cubic-bezier timing curves and duration constants.
5. `aero_math.json`: Specular reflection glare angles, glass blur parameters, text halo glow layers, and button pulse keyframes.
6. `slices.json`: 9-slice border coordinates and dimensional metadata for legacy raster parts.

### Generated Stylesheets (`gui/`)
The compiler deterministically generates three SCSS partials:
- `gui/_tokens.scss`: Emits all `--w7-*` root custom properties, animations, and keyframes.
- `gui/_aero-tints.scss`: Emits the 16 Aero personalization tints and non-composited basic/high-contrast theme overrides.
- `gui/_variables.scss`: Imports `_tokens.scss` and `_aero-tints.scss`, and maps legacy `--w7-el-*` variables to prevent regressions in unrefactored components.

---

## 3. PostCSS Compatibility & Static Inlining Architecture

The build system in `build.js` uses PostCSS with `postcss-nested`, `postcss-calc`, and `postcss-css-variables`.

### Constraints of `postcss-css-variables`
The `postcss-css-variables` plugin parses CSS custom properties at build time to produce the static distribution bundle `dist/7.inline.css`. This plugin can only inline variables statically defined directly on `:root`. Variables declared inside selector scopes (such as `[data-aero-tint="..."]`) cannot be resolved statically.

### Dual-Layer Solution
1. **Static Baseline on `:root`:** Default Aero tokens (Sky Blue tint, standard push button gradients, system metrics) are declared on `:root`. This allows `postcss-css-variables` to resolve all references during static bundling without compile errors.
2. **Dynamic Runtime Overrides:** The 16 personalization tints in `gui/_aero-tints.scss` override `--w7-aero-tint-color`, `--w7-aero-tint-rgb`, and related border variables at runtime. Browsers consuming `dist/7.css` or `dist/7.scoped.css` support full dynamic theming via data attributes.

---

## 4. Aero Personalization & Theme Fallbacks

Windows 7 allowed users to personalize window frames using 16 predefined Aero glass colors. `gui/_aero-tints.scss` implements these 16 tints with authentic RGB values and translucency levels:

| Tint Identifier | Display Name | Hex Code | Translucent RGBA |
| :--- | :--- | :--- | :--- |
| `default` | Sky (Default) | `#70a4c2` | `rgba(112, 164, 194, 0.65)` |
| `sky` | Sky | `#70a4c2` | `rgba(112, 164, 194, 0.65)` |
| `twilight` | Twilight | `#556882` | `rgba(85, 104, 130, 0.65)` |
| `smoke` | Slate / Smoke | `#646e78` | `rgba(100, 110, 120, 0.70)` |
| `pink` | Pink | `#c37199` | `rgba(195, 113, 153, 0.65)` |
| `frost` | Frost | `#e5ecf0` | `rgba(229, 236, 240, 0.70)` |
| `blush` | Blush | `#b8597c` | `rgba(184, 89, 124, 0.65)` |
| `ruby` | Ruby | `#ad3b48` | `rgba(173, 59, 72, 0.65)` |
| `pumpkin` | Pumpkin | `#c46931` | `rgba(196, 105, 49, 0.65)` |
| `sun` | Sun | `#cca42b` | `rgba(204, 164, 43, 0.65)` |
| `lime` | Lime | `#8fa83b` | `rgba(143, 168, 59, 0.65)` |
| `leaf` | Leaf | `#489445` | `rgba(72, 148, 69, 0.65)` |
| `sea` | Sea | `#417d8a` | `rgba(65, 125, 138, 0.65)` |
| `violet` | Violet | `#6f4eb8` | `rgba(111, 78, 184, 0.65)` |
| `fuchsia` | Fuchsia | `#913f8c` | `rgba(145, 63, 140, 0.65)` |
| `slate` | Slate | `#485966` | `rgba(72, 89, 102, 0.70)` |

### Non-Composited Theme Fallbacks
- **Windows Basic (`[data-theme="basic"]`):** Replaces DWM glass blur with opaque blue linear gradients (`linear-gradient(to bottom, #99b4d1 0%, #b9d1ea 100%)`) and flat 4px window borders (`#a0b4c8`).
- **High Contrast (`[data-theme="high-contrast"]`):** Disables translucent gradients, applying high-contrast solid borders (`#000000`), white window backgrounds, and standardized contrast boundaries.

---

## 5. Typography System & Subpixel Smoothing

Windows 7 used Segoe UI at 9pt (12px at 96 DPI) as the standard shell font. `gui/_typography.scss` establishes typography defaults across all elements:

1. **Font Family Hierarchy:**
   `'Segoe UI', 'Selawik', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif`
   `Selawik` is bundled in `assets/fonts/` as an open-source, metric-compatible Segoe UI replacement for non-Windows platforms.
2. **Subpixel Antialiasing:**
   Declared globally on `body`, `button`, `input`, `select`, and `textarea`:
   `-webkit-font-smoothing: antialiased;`
   `-moz-osx-font-smoothing: grayscale;`
   `text-rendering: optimizeLegibility;`
3. **Task Dialog & Instructional Typography Hierarchy:**
   - Primary Instruction (`.instruction-primary`): 12pt (`16px`), `#003399`, font-weight 400.
   - Secondary Description (`.instruction-secondary`, `.instruction-description`): 9pt (`11px`), `#555555`, line-height 1.3.
   - Caption Text (`.caption`, `small`): 8pt (`10.5px`), `#666666`.

---

## 6. Form Control Token Coverage (Expanded for Phase 2)

Ahead of component rebuilds in Phase 2, the token dictionary was expanded in `assets/tokens/colors.json` and `assets/tokens/metrics.json` to cover all form controls:

- **Push Buttons:** 6 visual states (normal, hover, pressed, default pulse, disabled, focused).
- **Command Links:** Hover and pressed background gradients, border states, and glyph metric parameters.
- **Text Inputs:** Normal, hover, focus (`#3d7bad`), and disabled background and border colors.
- **Checkboxes:** Normal, hover, pressed, disabled states, inner shadows, and `#1e395b` checkmark glyph colors.
- **Radio Buttons:** Radial background gradients for normal, hover, pressed, disabled states, and `#1e395b` center bullet gradient.
- **Sliders / Trackbars:** Groove track border and background, thumb states (normal, hover, pressed, disabled), and tick mark colors.
- **Spin Buttons:** Up/down chevron button states (normal, hover, pressed, disabled), divider lines, and arrow glyph colors.
- **Group Boxes:** Etched border groove (`#d9d9d9` with `#ffffff` inner highlight) and `#003399` legend text color.

---

## 7. Verification & Test Harness Audit

The test script `scripts/verify_stage_1.py` validates compliance across 47 individual checkpoints:

```
=== PHASE 1 VERIFICATION AUDIT ===
[PASS] Token file exists: colors.json
[PASS] Token file parses valid JSON: colors.json
[PASS] Token file exists: metrics.json
[PASS] Token file parses valid JSON: metrics.json
[PASS] Token file exists: typography.json
[PASS] Token file parses valid JSON: typography.json
[PASS] Token file exists: animations.json
[PASS] Token file parses valid JSON: animations.json
[PASS] Token file exists: aero_math.json
[PASS] Token file parses valid JSON: aero_math.json
[PASS] Token file exists: slices.json
[PASS] Token file parses valid JSON: slices.json
[PASS] _tokens.scss exists
[PASS] _aero-tints.scss exists
[PASS] _variables.scss exists
[PASS] _tokens.scss declares --w7-font-family
[PASS] _tokens.scss declares --w7-font-rendering
[PASS] _tokens.scss declares --w7-color-window-bg
[PASS] _tokens.scss declares --w7-color-window-text
[PASS] _tokens.scss declares --w7-glass-blur
[PASS] _tokens.scss declares --w7-glass-specular-angle
[PASS] _tokens.scss declares --w7-aero-tint-color
[PASS] _tokens.scss declares --w7-btn-bg
[PASS] _tokens.scss declares --w7-btn-hover-bg
[PASS] _tokens.scss declares --w7-btn-pressed-bg
[PASS] _tokens.scss declares --w7-btn-default-pulse-bg
[PASS] _tokens.scss declares --w7-checkbox-bg
[PASS] _tokens.scss declares --w7-radio-bg
[PASS] _tokens.scss declares --w7-slider-track-bg
[PASS] _tokens.scss declares --w7-spinner-btn-bg
[PASS] _tokens.scss declares --w7-groupbox-border
[PASS] _tokens.scss declares --w7-progress-normal-chunk
[PASS] _tokens.scss declares --w7-basic-title-active-bg
[PASS] _tokens.scss declares --w7-metric-window-border-width
[PASS] _tokens.scss declares --w7-metric-btn-height
[PASS] _tokens.scss declares --w7-metric-slider-thumb-width
[PASS] _tokens.scss declares --w7-ease-fast-entrance
[PASS] _tokens.scss declares --w7-dur-btn-pulse
[PASS] _tokens.scss has button pulse keyframes
[PASS] _tokens.scss has progress shimmer keyframes
[PASS] _aero-tints.scss contains all 16 Aero tints
[PASS] _aero-tints.scss has basic theme fallback
[PASS] _aero-tints.scss has high-contrast fallback
[PASS] _variables.scss imports _tokens.scss and _aero-tints.scss
[PASS] _variables.scss provides legacy aliases
[PASS] _typography.scss applies subpixel smoothing and text hierarchy
[PASS] Distribution bundles compiled (dist/7.css, dist/7.scoped.css, dist/7.inline.css)
[PASS] Safety audit script passes with zero violations
=== ALL PHASE 1 CHECKS PASSED ===
```

STATUS: PHASE 1 COMPLETE (READY FOR PHASE 2)
