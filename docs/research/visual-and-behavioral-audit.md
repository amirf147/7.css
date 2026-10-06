# Visual and Behavioral UI Audit Log

This document serves as the centralized defect register, raster-to-vector transition audit, and physical inspection guide for `7.css`. Rather than applying isolated, piecemeal patches that risk architectural inconsistency and style leakage, all visual discrepancies, contrast failures, and fidelity regressions are cataloged here with their root causes and verified Windows 7 specifications prior to batch remediation.

---

## 1. Defect and Observation Register

| ID | Component | Severity | Location | Status | Summary |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AUD-001** | Action Pane (`.action-pane`) | High | `docs/docs.css`, `layout.ejs` | Fixed | Floating column fixed to viewport middle across documentation pages |
| **AUD-002** | Window Caption (`.title-bar-text`) | High | `gui/_window.scss:410` | Triaged | Low contrast white text on white halo over translucent glass |
| **AUD-003** | Standalone Title Bar Demos | Medium | `docs/components/window/titlebar.ejs` | Triaged | Standalone `.title-bar` demos lack container contrast on white page body |
| **AUD-004** | Inactive Selection Contrast | Medium | `gui/_treeview.scss`, `gui/_listview.scss` | Triaged | Inactive window selections need validation against blurred backdrops |
| **AUD-005** | Dialog Backdrop Compositing | Low | `gui/_window.scss:346` | Triaged | Pure CSS `:target` dialogs lack dimming backdrop overlay |
| **AUD-006** | Caption Button Glyphs | High | `gui/icon/caption-*.svg`, `_window.scss:486` | Triaged | Flat black "X" and dark glyphs replace original white shaded icons |
| **AUD-007** | Push Button Pulse & Glow | High | `gui/_button.scss:58`, `_tokens.scss:82` | Triaged | Muted pale gray buttons lack authentic Windows 7 cyan breathing pulse |

---

## 2. Detailed Issue Records

### AUD-001: Floating Action Pane Layout Intrusion
- **Component:** MMC Utility Action Pane (`.action-pane`)
- **Affects:** Entire documentation layout (`http://127.0.0.1:3000/`)
- **Visual Symptom:** A tall vertical panel labeled "Actions" and "System" with links ("Open Saved Log...", "Properties") floats fixed over the center-left content area, covering headings and text across all documentation pages.
- **Root Cause:** In `docs/docs.css`, the global `aside` selector was unscoped. When `docs/components/layout.ejs` rendered `<aside class="action-pane">`, that element inherited viewport-fixed positioning without an explicit `left` coordinate, anchoring it at its static document offset (~260px from the left margin) directly over main documentation copy.
- **Architectural Solution:** Scoped sidebar layout rules in `docs/docs.css` to `body > aside` and assigned explicit `left: 0`.
- **Status:** Fixed and verified.

---

### AUD-002: Window Title Bar Text Contrast and Halo Bleed
- **Component:** Window Title Bar Text (`.title-bar-text`)
- **Affects:** All standard `.window.active` instances, including the introductory demo window.
- **Visual Symptom:** Caption text ("My First Program") appears washed out, blurry, and difficult to read against translucent Aero glass.
- **Technical Root Cause:** In `gui/_window.scss` line 410, `.title-bar-text` specifies `color: #ffffff;` combined with `text-shadow: var(--w7-glass-text-halo-active);` (a 10px multi-stop white glow). Both the text body and the halo shadow are pure white (`#ffffff`). Over a light glass tint or white documentation canvas, the contrast ratio is approximately 1.3:1, failing WCAG 2.1 AA standards (minimum 4.5:1).
- **Windows 7 Historical Specification:** In native Windows 7 Aero (DWM), the active window title bar font color is dark charcoal or pure black (`#000000`, defined in `assets/tokens/colors.json` line 323). Microsoft engineered the diffuse white halo (`DrawThemeTextEx` with `DTT_GLOWSIZE`) to ensure black text remained legible when dragged over dark desktop wallpapers.
- **Planned Architectural Solution:**
  1. In `gui/_tokens.scss`, declare `--w7-titlebar-active-text: #000000;` and `--w7-titlebar-inactive-text: #4c4c4c;`.
  2. Set `.title-bar-text { color: var(--w7-titlebar-active-text, #000000); }` in `gui/_window.scss`.
  3. Under `[data-theme="vista-basic"]`, override `--w7-titlebar-active-text: #ffffff;`.
- **Status:** Triaged. Queued for batch remediation.

---

### AUD-003: Standalone Title Bar Isolation in Documentation Examples
- **Component:** Title Bar Sample (`docs/components/window/titlebar.ejs`)
- **Affects:** Isolated title bar code examples.
- **Visual Symptom:** Standalone title bar examples render without an enclosing `.window` frame directly on the white documentation canvas, lacking boundary context.
- **Root Cause:** Examples render `<div class="title-bar">` directly. In `gui/_window.scss`, `.title-bar` background has translucent gradient stops designed to composite over `--w7-w-bg`.
- **Planned Architectural Solution:** Wrap standalone title bar demos inside a bounded preview wrapper with a neutral background or border container.
- **Status:** Triaged.

---

### AUD-004: Inactive Selection Contrast on Explorer Controls
- **Component:** TreeView (`_treeview.scss`), ListView (`_listview.scss`)
- **Affects:** Unfocused list and tree selections.
- **Visual Symptom:** Gray inactive selection states (`#dedede`) may blend into adjacent frame backgrounds when windows lose focus.
- **Planned Architectural Solution:** Verify contrast ratio of inactive selection tokens against `--w7-surface` (`#ffffff`) and table alternate row zebra striping.
- **Status:** Triaged.

---

### AUD-005: Dialog Modal Overlay Presentation
- **Component:** Dialog Box (`_window.scss:346`)
- **Affects:** `[role="dialog"]`
- **Visual Symptom:** Pure CSS `:target` modal displays without a dimming backdrop scrim, allowing underlying page elements to visually interfere with dialog contents.
- **Planned Architectural Solution:** Evaluate pure CSS backdrop pseudo-element or document recommendation for standard HTML5 `<dialog>` support.
- **Status:** Triaged.

---

### AUD-006: Caption Button Glyph Silhouette Regression
- **Component:** Caption Buttons (`gui/icon/caption-*.svg`, `gui/_window.scss:486-560`)
- **Affects:** Window Minimize, Maximize, Restore, and Close buttons at rest.
- **Visual Symptom:** The close button displays a flat, stark black "X", and minimize/maximize display flat black geometric lines. In the original `7.css`, these glyphs were clean white with subtle depth and shadow drops.
- **Technical Root Cause:** When transitioning from 1x raster PNGs (`close.png`, `minimize.png`, `maximize.png`) to SVGs in Phase 3, the SVGs were authored as primitive single-color black vectors (`fill="#000000"`). They only switch to white on hover. In native Windows 7 Aero, resting caption glyphs are white with a soft bottom drop shadow (`drop-shadow(0 1px 0 rgba(0, 0, 0, 0.45))`).
- **Planned Architectural Solution:**
  1. Re-author `caption-close.svg`, `caption-minimize.svg`, `caption-maximize.svg`, `caption-restore.svg`, and `caption-help.svg` with authentic white fills (`fill="#ffffff"`).
  2. Embed a subtle dark drop shadow filter or apply `filter: drop-shadow(0 1px 1px rgba(0, 0, 0, 0.5))` in `_window.scss`.
- **Status:** Triaged. Queued for batch remediation.

---

### AUD-007: Push Button Default Breathing Pulse & Cyan Hover Bloom Regression
- **Component:** Push Buttons (`gui/_button.scss:58-77`, `gui/_tokens.scss:82`)
- **Affects:** Standard push buttons, `.default` buttons, and submit buttons.
- **Visual Symptom:** The introductory "OK" button displays flat gray with an almost invisible border pulse. In the original `7.css`, `.default` buttons radiated a vivid cyan-blue breathing gradient, and buttons bloomed cyan on hover.
- **Technical Root Cause:**
  1. The original `7.css` used a dual-layer cyan background gradient:
     `radial-gradient(circle at bottom, #2aceda, transparent 65%), linear-gradient(#b6d9ee 50%, #1a6ca1 50%)`
     with a keyframe animation cycling an inset cyan box-shadow (`#34deffdd`).
  2. Phase 2 replaced this with token `--w7-btn-hover-bg`, which was set to a muted, pale sky-blue gradient (`#eaf6fd` to `#a7d9f5`). Furthermore, `&.default` in `_button.scss` had its background left as default gray, animating only `border-color` and `box-shadow`.
- **Planned Architectural Solution:**
  1. Restore the authentic cyan-blue gradient stops in `--w7-btn-default-bg` and `--w7-btn-hover-bg`.
  2. Rebind `.default` buttons to display the cyan gradient background and cycle the inset cyan glow pulse.
- **Status:** Triaged. Queued for batch remediation.

---

## 3. Raster vs. Vector Transition Audit & Investigation

### Architectural Verdict on the Vector Migration
The decision to migrate from 1x raster PNGs to resolution-independent SVG vectors was **technically correct and necessary**.

The visual issues identified do not stem from vector technology, but from **asset authoring fidelity**:

1. **Why 1x Raster PNGs are Deprecated:**
   The original `7.css` raster PNGs (`close.png`, `minimize.png`, `maximize.png`) were fixed at 10x9 pixels. On modern high-DPI displays (125%, 150%, 200%, Retina, 4K), 1x PNGs suffer from subpixel blurring, scaling distortion, or rigid pixelation (`image-rendering: pixelated`).
2. **Where the Phase 3 Vector Migration Erred:**
   The vector SVGs were created as flat, black-filled geometric silhouettes without the gradient depths, white fills, and drop shadows present in the Windows 7 DWM compositor.
3. **The Solution (Fidelity Tuning vs. Reversion):**
   Discarding the vector architecture or rolling back to 2020 raster files would reintroduce high-DPI blurriness and break theme adaptability. The correct approach is upgrading the vector definitions and CSS filters to replicate the visual fidelity of the original design.

### Transition Inventory Matrix

| Control Category | Original 7.css Implementation | Current Vector Implementation | Fidelity Status | Action Required |
| :--- | :--- | :--- | :--- | :--- |
| **Caption Glyphs** | 1x PNGs (`close.png`, `minimize.png`) | Flat black SVGs (`caption-close.svg`) | **Degraded** | Re-author SVGs with white fill and 1px drop shadow filter. |
| **Push Button Glass** | CSS dual-layer radial/linear gradient | CSS single linear gradient | **Degraded** | Restore rich cyan radial base gradient and breathing pulse. |
| **TreeView Chevrons** | Ad-hoc border triangles | Scalable SVG chevrons (Phase 4) | **Superior** | Retain vector chevrons (resolution-independent, sharp). |
| **Scrollbar Arrows** | 1x PNGs (`button-up.png`) | Clean SVG arrows (Phase 4) | **Superior** | Retain vector arrows. |
| **Command Link Glyphs**| Missing / partial | Authentic green arrow SVG (Phase 2) | **Superior** | Retain vector glyph. |
| **Task Dialog Emblems**| None | Vector shield, info, warning, error | **Superior** | Retain vector emblems. |
| **Slider Thumbs** | 1x PNGs (`slider-indicator.png`) | 1x PNGs (Retained from original) | **Pending** | Plan high-DPI vector transition in Phase 5. |

---

## 4. Physical Visual Audit Protocol

When reviewing the documentation and components in person at `http://127.0.0.1:3000/`, follow this systematic procedure:

### Step 1: Optical Contrast and Background Variance
Inspect each component against three background environments:
1. Pure white document body (`#ffffff`).
2. Photographic desktop canvas (`.background` wallpaper container).
3. Dark / solid canvas (`.window.maximized` or dark container).
- Check that text elements maintain a minimum 4.5:1 contrast ratio.
- Check that white text halos do not wash out text glyphs.

### Step 2: State Machine Completeness
For every interactive control (Buttons, Checkboxes, Dropdowns, TreeViews, Tabs):
1. **Normal / Default:** Check resting borders, gradients, and font baseline.
2. **Hover:** Confirm subtle brightness or cyan back-glow activation.
3. **Active / Pressed:** Verify inset shadow displacement (1px text shift where applicable) and darkened gradient.
4. **Focused (`:focus-visible`):** Ensure dotted focus rectangle is visible without clipping.
5. **Disabled:** Verify 40% opacity or grayed icon filter (`filter: grayscale(1) opacity(0.5)`).

### Step 3: Aero Glass Metrics and Geometry
1. Restored window corner radius: 6px for Windows 7 (`--w7-metric-window-radius`), 8px for Vista.
2. Caption button dimensions: 43px width x 19px height (Close button 45px width).
3. Window border padding: 6px surrounding window body.
4. Sizing grip alignment on status bars.

### Step 4: Documentation Layout and Scoping
1. Confirm that sidebar navigation remains pinned to the left margin (`left: 0`, width 240px).
2. Confirm that main content maintains a 260px left margin without horizontal overlap.
3. Resize the browser below 480px width to ensure sidebar collapses and content flows cleanly.

---

## 5. Recommended Execution Plan

To restore visual excellence without architectural regression, execute the following remediation batch:

1. **Batch Remediation Step 1: Caption Glyph Vectors (AUD-006)**
   Update `caption-*.svg` assets to authentic white fills and bind soft dark drop-shadow filters.
2. **Batch Remediation Step 2: Push Button Cyan Bloom (AUD-007)**
   Restore the vivid dual-layer cyan background gradient and pulsating glow on `.default` and hover push buttons.
3. **Batch Remediation Step 3: Active Caption Contrast (AUD-002)**
   Bind `.title-bar-text` to `#000000` with the diffuse white halo glow.
4. **Batch Remediation Step 4: Desktop Canvas Preview Stage**
   Wrap documentation window demos in an authentic desktop stage container so Aero glass optics render against realistic wallpaper textures.
5. **Batch Remediation Step 5: Interactive Theme Switcher**
   Implement a live header dropdown allowing instant toggling between Windows 7 Aero, Windows Vista Aero, and Windows Vista Basic.
