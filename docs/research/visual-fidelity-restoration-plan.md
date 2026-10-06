# Visual Fidelity Restoration Plan: Windows 7 Aero Parity

## 1. Executive Summary & Problem Statement

During the Phase 2 and Phase 3 refactoring of `7.css`, legacy ad-hoc raster assets and hardcoded inline styles were migrated to a CSS custom property token dictionary and vector SVGs. While this established a modular architecture and passed automated syntax tests, visual inspection against the canonical `7.css` window (documented in `docs/window.png` and historical screenshots) revealed three distinct visual regressions:

1. **Caption Button Glyphs:** Window caption controls (`gui/icon/caption-close.svg`) were drawn as flat black silhouettes (`fill="#000000"`) without drop shadows, replacing authentic white glyphs with subtle depth.
2. **Push Button Gel Glow & Pulse:** The `.default` button lost its vivid cyan-blue gel background (`radial-gradient`) and breathing glow animation, flattening into a muted gray button with an imperceptible border pulse.
3. **Title Bar Caption Contrast:** `.title-bar-text` in `gui/_window.scss` hardcoded `color: #ffffff;` over a 10px white halo, producing an unreadable 1.3:1 contrast ratio against light Aero glass.
4. **Documentation Canvas Presentation:** Translucent Aero glass windows sit on bare white document copy without an underlying wallpaper texture, preventing the `backdrop-filter: blur(...)` engine from demonstrating authentic refraction and depth.
5. **Theme Switcher Absence:** No interactive control exists in the documentation interface to switch live between Windows 7 Aero, Windows Vista Aero, and Windows Vista Basic.

This document outlines the deterministic, step-by-step implementation plan to resolve these regressions in a single coordinated batch without reverting to 1x raster assets.

---

## 2. Architecture & File Inventory

The remediation touches six core modules across tokens, styles, assets, and documentation:

```
7.css/
├── assets/tokens/
│   └── colors.json               # Canonical token color stops
├── gui/
│   ├── icon/
│   │   ├── caption-close.svg     # Re-author: white fill with shadow
│   │   ├── caption-minimize.svg  # Re-author: white fill with shadow
│   │   ├── caption-maximize.svg  # Re-author: white fill with shadow
│   │   ├── caption-restore.svg   # Re-author: white fill with shadow
│   │   └── caption-help.svg      # Re-author: white fill with shadow
│   ├── _tokens.scss              # Regenerate token variables
│   ├── _variables.scss           # Token aliases
│   ├── _button.scss              # Button cyan gradient and breathing pulse
│   └── _window.scss              # Title text color binding & caption filters
├── docs/
│   ├── docs.css                  # .desktop-stage preview container
│   ├── script.js                 # Live theme switcher handler
│   ├── sections/
│   │   ├── intro.ejs             # Wrap demo window in desktop stage
│   │   └── navigation.ejs        # Add theme switcher UI widget
│   └── components/window/
│       └── titlebar.ejs          # Wrap standalone title bar demos
└── scripts/
    ├── generate_tokens.py        # Token compiler
    ├── verify_stage_2.py         # Push button verification suite
    └── verify_stage_3.py         # Window and caption verification suite
```

---

## 3. Step-by-Step Technical Execution

### Task 1: Re-author Caption Button Vector Glyphs (AUD-006)

#### Problem
`caption-close.svg`, `caption-minimize.svg`, `caption-maximize.svg`, `caption-restore.svg`, and `caption-help.svg` were authored with `fill="#000000"`. They only turned white on hover, displaying as stark flat black markings at rest.

#### Implementation Steps
1. Re-author each SVG in `gui/icon/` with `fill="#ffffff"` and authentic stroke geometries.
2. In `gui/_window.scss`, bind a subtle dark drop shadow filter to caption glyph pseudo-elements:
   ```scss
   &::before {
     content: "";
     position: absolute;
     top: 0;
     bottom: 0;
     left: 0;
     right: 0;
     background-repeat: no-repeat;
     background-position: center;
     pointer-events: none;
     filter: drop-shadow(0 1px 1px rgba(0, 0, 0, 0.45));
   }
   ```
3. Update `scripts/verify_stage_3.py` to validate white caption glyph bindings.

---

### Task 2: Restore Push Button Cyan Bloom and Breathing Pulse (AUD-007)

#### Problem
In `gui/_button.scss`, `.default` buttons only pulse their border and box-shadow, leaving the background as flat gray. The hover gradient in `--w7-btn-hover-bg` was muted to pale pastel sky-blue.

#### Implementation Steps
1. In `assets/tokens/colors.json` and `gui/_tokens.scss`, restore the authentic dual-layer cyan background gradient:
   ```scss
   --w7-btn-default-bg: radial-gradient(circle at bottom, #2aceda, transparent 65%), linear-gradient(#b6d9ee 50%, #1a6ca1 50%);
   --w7-btn-hover-bg: radial-gradient(circle at bottom, #2aceda, transparent 65%), linear-gradient(#b6d9ee 50%, #1a6ca1 50%);
   ```
2. In `gui/_button.scss`, restore the breathing pulse keyframe sequence cycling the cyan glow:
   ```scss
   @keyframes w7-aero-button-pulse {
     0%, 100% {
       border-color: #5586a3;
       box-shadow: inset 0 0 3px 1px rgba(52, 222, 255, 0.85), 0 0 2px rgba(52, 222, 255, 0.5);
     }
     50% {
       border-color: #2c688d;
       box-shadow: inset 0 0 6px 2px rgba(52, 222, 255, 1.0), 0 0 8px rgba(52, 222, 255, 0.85);
     }
   }
   ```
3. Bind `background: var(--w7-btn-default-bg);` to `.default` and `input[type="submit"]`.
4. Ensure `[data-theme="vista"] button` retains its authentic Vista split-horizon gradient overrides.

---

### Task 3: Restore Black Caption Text with White Halo (AUD-002)

#### Problem
In `gui/_window.scss`, `.title-bar-text` specifies `color: #ffffff;` over `--w7-glass-text-halo-active` (a 10px white glow), washing out caption text over translucent glass.

#### Implementation Steps
1. In `gui/_tokens.scss`, declare token `--w7-titlebar-active-text: #000000;`.
2. In `gui/_window.scss`, update `.title-bar-text`:
   ```scss
   &-text {
     color: var(--w7-titlebar-active-text, #000000);
     font-weight: var(--w7-font-weight-bold, 700);
     letter-spacing: 0;
     line-height: 15px;
     display: flex;
     align-items: center;
     gap: 6px;
     text-shadow: var(--w7-glass-text-halo-active);
     white-space: nowrap;
     overflow: hidden;
     text-overflow: ellipsis;
   }
   ```
3. In `gui/_aero-tints.scss`, verify that `[data-theme="vista-basic"]` overrides `--w7-titlebar-active-text: #ffffff;` to preserve readability against the dark solid navy caption bar.

---

### Task 4: Documentation Desktop Wallpaper Stage

#### Problem
Aero glass optics require an underlying image or texture to demonstrate frosted glass blur and specular highlights. Placing windows on plain `#ffffff` document margins flattens the aesthetic.

#### Implementation Steps
1. In `docs/docs.css`, define `.desktop-stage`:
   ```css
   .desktop-stage {
     position: relative;
     padding: 32px;
     margin: 24px 0;
     border-radius: 4px;
     border: 1px solid #c0c0c0;
     background-image: url("./flower-aaronburden-unsplash.jpg");
     background-position: center;
     background-size: cover;
     box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.25);
     overflow: hidden;
   }
   ```
2. In `docs/sections/intro.ejs`, wrap the introductory window in `.desktop-stage`.
3. In `docs/components/window/titlebar.ejs`, wrap standalone title bar code samples inside bounded stage containers so captions do not sit on white canvas.

---

### Task 5: Interactive Theme Switcher Dropdown in Documentation UI

#### Problem
The documentation currently lacks an interactive UI control to toggle themes live. Users cannot view Windows Vista Aero or Windows Vista Basic without manually editing HTML attributes.

#### Implementation Steps
1. In `docs/sections/navigation.ejs`, insert a theme switcher widget above the tree view:
   ```html
   <div class="theme-switcher-box" style="padding: 8px 12px; border-bottom: 1px solid #dfdfdf;">
     <label for="theme-selector" style="font-size: 8pt; color: #555; display: block; margin-bottom: 4px;">Theme Engine:</label>
     <select id="theme-selector" style="width: 100%; font-size: 8.5pt;">
       <option value="win7">Windows 7 Aero (Default)</option>
       <option value="vista">Windows Vista Aero</option>
       <option value="vista-basic">Windows Vista Basic</option>
     </select>
   </div>
   ```
2. In `docs/script.js`, bind the theme switcher logic:
   - On change, set `data-theme` attribute on `document.body` or remove it for Windows 7 default.
   - Persist user choice in `localStorage.getItem("7css-theme")`.
   - Restore stored theme on initial page load.

---

### Task 6: Automated Verification and Build Pipeline Validation

#### Implementation Steps
1. Re-run `py -3.10 scripts/generate_tokens.py` to compile updated tokens into `gui/_tokens.scss` and `gui/_aero-tints.scss`.
2. Update verification suites (`scripts/verify_stage_2.py` and `scripts/verify_stage_3.py`) to assert:
   - White caption glyph SVG fills.
   - Dual-layer cyan gradient tokens on push buttons.
   - Black active caption text binding with white halo.
3. Run `npm run build` and `npm test` to verify that all 150+ automated checkpoints pass.

---

## 4. Verification Checkpoints & Acceptance Criteria

| Checkpoint | Expected Result | Pass Criteria |
| :--- | :--- | :--- |
| **Close Button Glyph** | Crisp white "X" with subtle drop shadow at rest; crimson red on hover with white "X". | Matches Image 2; no flat black "X". |
| **Minimize / Maximize** | Crisp white line and window box with subtle drop shadow at rest; cyan glow on hover. | Matches Image 2; no flat black lines. |
| **"OK" Button (.default)** | Luminous cyan-blue radial gel background with breathing cyan glow animation. | Matches Image 2; not flat gray. |
| **Title Bar Caption** | Pure black text `#000000` with luminous white halo glow on active window. | WCAG contrast ratio >= 4.5:1; matches Image 2. |
| **Glass Refraction** | Frosted glass blurs underlying desktop wallpaper stage. | Glass optics visible; no washed-out flat white title bar. |
| **Live Theme Switcher** | Toggling dropdown in navigation sidebar instantly switches entire page between Win7 Aero, Vista Aero, and Vista Basic. | Theme attributes update cleanly without reload. |
| **Automated Tests** | `npm test` executes all verification scripts with zero failures. | 100% checks passing. |

---

## 5. Execution Command Sequence for New Chat Session

When starting the new chat window to execute this plan, prompt the agent with:

```text
Please execute the visual fidelity restoration plan documented in:
docs/research/visual-fidelity-restoration-plan.md

Follow Tasks 1 through 6 sequentially:
1. Re-author caption button vector SVGs (white fill with shadow drop).
2. Restore push button cyan gel background and breathing pulse in gui/_button.scss.
3. Restore black active caption text with white halo in gui/_window.scss.
4. Implement .desktop-stage in docs/docs.css and wrap demo windows.
5. Add interactive theme switcher dropdown to docs navigation.
6. Verify via scripts/generate_tokens.py, npm run build, and npm test.
```
