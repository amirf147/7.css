# Windows 7 UI Architecture: Comprehensive Feature & Component Catalog

This document establishes the exhaustive feature taxonomy of the Windows 7 user interface across all system shells, windows, consoles, navigation controls, and micro-interactions. It serves as the long-term scope reference for `7.css` component authoring and showcase template construction.

---

## 1. Desktop & Shell Surface

### 1.1 The "Superbar" (Taskbar)
Windows 7 redesigned the taskbar from Windows XP's 30px labeled bar into a 40px glass application launcher and window manager.

- **Start Orb:**
  - 36px circular glass emblem overlapping the top edge of the taskbar by 4px.
  - Normal state: Translucent frosted glass orb displaying the Windows flag.
  - Hover state: Multi-directional radial back-glow in red, green, blue, and yellow quadrants.
  - Pressed state: Darkened inset bevel with intensified core luminance.
- **Taskbar Application Tiles:**
  - 40px square icon-only buttons (no text labels by default).
  - Normal state: Transparent button with subtle border line.
  - Hover state: Translucent light-blue frosted glass tile with inner specular border.
  - Active/Focused window: Distinct raised glass button with persistent illumination.
  - Alert state: Flashing orange glow cycling between `#ff9900` and `#ffcc00`.
  - Taskbar Progress Overlay: Green, yellow, or red progress bar rendered directly across the tile background behind the application icon.
- **Thumbnail Previews (Aero Peek):**
  - Floating card anchored above taskbar tiles with `backdrop-filter: blur(20px)` and white inner border.
  - Header: 16px application icon, window title in Segoe UI 9pt bold, red hover close button (`X`).
  - Body: Live thumbnail preview image surrounded by a 1px border.
  - Transport Controls (Mini Toolbar): Play, Pause, Next, Previous buttons embedded in the preview footer for media applications.
- **Jump Lists:**
  - Specialized context menus anchored to taskbar items.
  - Categorized into "Pinned", "Recent", "Frequent", and "Tasks".
  - Section dividers: 1px horizontal gray rules (`#d9d9d9`).
  - Right-aligned pushpin icons on hover to pin or unpin items.
- **Notification Area (System Tray) & Overflow Menu:**
  - Chevron trigger button (`^`) opening a floating glass popup container housing hidden notification icons.
  - Action Center Flag: Displays dynamic alert badges (red circle with white `X` for critical alerts, yellow triangle for maintenance suggestions).
  - Clock & Calendar Flyout: Clicking the tray clock reveals an analog clock with sweeping second hand alongside a monthly calendar picker.
- **Show Desktop Peek Slivers:**
  - 12px vertical glass rectangle at the extreme right corner of the taskbar.
  - Hovering triggers Aero Peek (instantly renders all open windows as transparent glass frames).
  - Clicking minimizes all windows to reveal the desktop.

---

### 1.2 Desktop Gadgets (Windows Sidebar Engine)
Windows 7 removed the fixed right-hand sidebar dock from Vista, allowing gadgets to float freely anywhere on the desktop canvas.

- **Gadget Control Bezel (Hover Frame):**
  - Appears only when the mouse hovers over the gadget perimeter.
  - Floating vertical strip with dark translucent glass containing:
    - Close button (`X`).
    - Settings wrench button (opens configuration flyout).
    - Drag handle grid icon.
- **Canonical Standard Gadgets:**
  - **CPU & RAM Meter:** Dual circular analog dials with metallic needles, gauge tick marks, and percentage readouts inside brushed aluminum and glass rings.
  - **Analog Clock:** Circular glass bezel with customizable faceplates, roman/standard numerals, hour/minute hands, and red sweep second hand.
  - **Calendar:** Two-tone date pad with orange header strip displaying month/year and white body displaying the numerical day.
  - **Weather Flyout:** Glass card showing live temperature, city label, and illustrated weather condition graphics.

---

### 1.3 The Start Menu
The Windows 7 Start Menu uses a two-pane asymmetric layout set inside an Aero Glass outer frame.

- **Left Pane (White Surface):**
  - Background: Solid white `#ffffff`.
  - Content: Pinned applications at the top, dynamic Recent Programs list below, separated by a 1px divider.
  - Selection: Light-blue gradient capsule hover state with right-pointing arrow triggering Jump Lists.
  - Search Box: Positioned at bottom left. Contains placeholder text "Search programs and files", embedded magnifying glass, and instant blue glow border on focus.
- **Right Pane (Translucent Dark Glass Surface):**
  - Background: Dark slate gradient glass (`rgba(30, 45, 60, 0.85)`).
  - Header: User account profile picture set inside a white-bordered square frame.
  - System Navigation Links: Documents, Pictures, Music, Games, Computer, Control Panel, Devices and Printers, Default Programs, Help and Support.
  - Footer Action: Segmented "Shut down" commit button with adjacent flyout arrow button (Restart, Sleep, Hibernate, Log off, Switch user, Lock).

---

## 2. Window Shell & Explorer Extensions

### 2.1 Aero Glass Title Bars & Window Frames
- **Restored State:**
  - Translucent blurred glass title bar and window borders (`backdrop-filter: blur(20px)`).
  - Ambient diagonal glare reflection overlay.
  - 6px border radius.
  - Outer drop shadow simulating DWM window depth.
- **Maximized State:**
  - Solid opaque dark glass backing (100% opacity, no desktop wallpaper bleed-through).
  - 0px border radius with borders tucked against the screen edges.
  - Caption buttons aligned directly against the top-right corner.
- **Inactive Window State:**
  - Desaturated slate gray tint.
  - Specular glare opacity reduced to 25%.
  - Title text shifts to gray (`#4c4c4c`) with reduced halo glow.
- **Aero Wizard Layout:**
  - Circular Back button embedded directly inside the top glass title bar adjacent to the title text.
  - Pure white canvas body without beveled frame margins.
  - Bottom command strip with Back, Next, Cancel buttons.

---

### 2.2 Caption Buttons (Min, Max, Restore, Close)
- Layout: Horizontal cluster of 3 glass buttons positioned in the top-right corner of the title bar.
- Normal State: Translucent glass pills with subtle inner border highlight.
- Hover (Minimize & Maximize): Cyan radial back-glow radiating behind the button glyph.
- Hover (Close Button): Crimson red gradient fill (`#e04343` to `#c82020`) with radial red back-glow.
- Pressed State: Darkened depression gradient with 1px inset drop shadow.

---

### 2.3 Explorer Navigation & Toolbars
- **Breadcrumb Address Bar:**
  - Segmented navigation capsules (`Computer` > `Local Disk (C:)` > `Windows`).
  - Hover state highlights individual segments as discrete rounded pills.
  - Triangle dropdown glyphs between segments display instant subfolder menus.
  - Far-right cluster: Embedded Refresh button and Stop button.
- **Instant Search Box:**
  - Embedded inside the address bar row.
  - Magnifying glass icon on the left, clear `X` icon on the right (visible when text is present).
  - Blue focus glow border.
  - Pop-down filter menu for file size, date modified, and file type.
- **Explorer Command Bar:**
  - Flat toolbar replacing classic Win32 menu bars.
  - Buttons: `Organize`, `Include in library`, `Share with`, `Burn`, `New folder`.
  - Hover state: Very subtle pale blue linear gradient with 1px border.
  - Split buttons: Discrete drop-down arrow section triggering options menus.
- **Navigation Pane (Left Sidebar):**
  - Hierarchical tree containing Quick Access/Favorites, Libraries, Homegroup, Computer, Network.
  - Uses Vista/7 transparent triangular chevrons (`GLPS_CLOSED`, `GLPS_OPENED`) rather than classic square `+`/`-` boxes.
- **Details Pane (Bottom Explorer Strip):**
  - Horizontal status banner across the window bottom.
  - Left: 48px or 64px file preview thumbnail.
  - Center: Metadata fields (file name, size, date modified, author).
  - Right: Interactive 5-star rating widget and editable tag inputs.
- **Preview Pane (Right Explorer Split):**
  - Vertical split panel toggled via command bar icon.
  - Displays full live document or image previews.

---

## 3. Systems Consoles & Administrative UIs

### 3.1 MMC 3.0 / Event Viewer
- **3-Pane Architecture:**
  - Left Pane (Scope Tree): TreeView navigation of log categories (Application, Security, Setup, System).
  - Center Pane (Results Grid): Multi-column ListView with sorting headers and event level glyphs (Error red circle with `X`, Warning yellow triangle, Information blue `i`).
  - Bottom Pane (Preview / Details): Split pane with `General` and `Details` (XML) tabs rendering log text.
  - Right Pane (Action Pane): Grouped category headers, task links, and action buttons.
- **Splitter Dividers:**
  - 4px vertical and horizontal divider bars with resize cursor indicators (`col-resize`, `row-resize`).

---

### 3.2 Control Panel Architecture
- **Aero Header Banner:**
  - Top horizontal banner with pale blue gradient fill, circular Back/Forward navigation discs, title, and search input.
- **Category View:**
  - Two-column grid layout.
  - Each item includes:
    - 48px high-DPI icon on the left.
    - 10pt bold primary category heading in `#003399` (e.g., `System and Security`, `Network and Internet`, `Hardware and Sound`).
    - Unordered list of secondary task hyperlinks in `#0066cc` underneath.
- **Classic Icon View:**
  - Responsive multi-column grid of 32px or 48px icons with labels centered below.

---

### 3.3 Task Dialogs & User Account Control (UAC)
- **Task Dialog Layout:**
  - Top Area: Pure white background, 32px status icon, 12pt primary instruction header in `#003399`, 9pt secondary body text.
  - Command Area: Command links with green arrow glyphs or radio buttons.
  - Expando Area: Collapsible `[>] See details` toggle link revealing debug text.
  - Footer Bar: Light gray `#f0f0f0` surface separated by a 1px border (`#dfdfdf`), right-aligned commit buttons (OK, Cancel).
- **UAC Elevation Modal:**
  - Desktop Dimming: Semi-transparent black backdrop simulating the Secure Desktop (`#000000` at 70% opacity).
  - Shield Header: Four-quadrant multi-color shield icon (blue, yellow, green, red).
  - Verification Badge: Gold/yellow banner for unverified publishers; blue banner for verified administrative software.

---

## 4. Informational Feedback & Micro-interactions

### 4.1 ScreenTips (Rich Tooltips)
- Replaced flat yellow tooltip boxes with styled popovers.
- Appearance: White linear gradient background, 1px `#767676` border, subtle drop shadow, 3px border radius.
- Structure:
  - Header: 16x16 icon, 9pt bold title text in `#003399` or black.
  - Body: 9pt regular explanatory text.
  - Shortcut indicator: Gray hint text (e.g., `Ctrl + S`).

---

### 4.2 Infobars (Notification & Security Banners)
- Location: Pinned immediately below the command bar or address bar.
- Appearance: Soft yellow gradient background (`#fff9d9` to `#ffebaa`), 1px amber border (`#e5c365`).
- Contents: Warning or shield icon on the left, descriptive notification text, blue action hyperlink, and close `X` button on the right.

---

### 4.3 Balloon Notifications
- Location: Anchored to notification area icons or form controls.
- Appearance: Rounded speech balloon with curved directional pointer tail.
- Close Button: Small gray `X` in top-right corner.
- Audio: Accompanied by `Windows Balloon.wav`.

---

### 4.4 The Question of "Clippy"
- **Historical Reality:**
  - Microsoft Office Assistant (Clippy / Clippit) was disabled by default in Office XP (2001), deprecated in Office 2003, and removed entirely in Office 2007.
  - Windows Agent (`msagent.exe`) was excluded from Windows 7 installations.
  - Clippy is an Office 97 through 2003 artifact, not a native Windows 7 element.
- **Recommended Architectural Role:**
  - Do not bundle Clippy in `7.css` core styles.
  - If a desktop assistant or companion is desired for the portfolio, provide it as an optional add-on script using the balloon notification component for dialogue boxes.

---

---

## 5. Authentication, Security Hub & Lock Screens

### 5.1 The Logon / Welcome Screen
- **Background Surface:** Default Windows 7 blue harmonic wallpaper with central glowing Windows emblem, illuminated glass leaves, and floating dandelion seeds.
- **User Account Tile:**
  - 128px square user avatar frame with rounded corners (4px) and soft white ambient drop shadow.
  - User name: Segoe UI, 16pt regular, white text with soft dark drop shadow (`text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8)`).
- **Authentication Controls:**
  - Password Input: White text box with inner shadow, rounded border, and right-aligned blue circle submit arrow button (`-->`).
  - Ease of Access button: Blue circle icon in bottom-left corner.
  - Power Options: Shutdown button with flyout menu (Restart, Sleep, Hibernate) in bottom-right corner.
  - "Switch User" command link pill centered below password input.

---

### 5.2 The Security Hub (Ctrl + Alt + Delete Screen)
- **Overlay Surface:** Fullscreen dark tinted backdrop over logon wallpaper (`rgba(0, 0, 0, 0.65)`).
- **Action Menu:** Centered vertical stack of wide glass command tiles:
  - `Lock this computer`
  - `Switch User`
  - `Log off`
  - `Change a password...`
  - `Start Task Manager`
- **Cancel Button:** Standard 75x23px command button centered below action tiles.

---

## 6. System Telemetry & Task Manager

### 6.1 Windows 7 Task Manager (taskmgr.exe)
- **Structure:** Classic 6-tab navigation container (`Applications`, `Processes`, `Services`, `Performance`, `Networking`, `Users`).
- **Performance Tab Oscilloscope Graphs:**
  - 3D Inset graph trenches with dark background (`#000000`).
  - Bright green grid lines (`rgba(0, 128, 0, 0.4)`).
  - Real-time CPU Usage and CPU History scrolling waveform in neon green (`#00ff00`).
  - Memory meter bar displaying committed versus physical memory.
- **Processes Tab:**
  - Sortable ListView with columns (`Image Name`, `PID`, `User Name`, `CPU`, `Memory`).
  - "Show processes from all users" button with UAC elevation shield icon.
  - "End Process" button right-aligned in footer.
- **Minimal Float Mode:**
  - Double-clicking the outer graph frame strips away the title bar, menu bar, and tabs, leaving a floating, resizable CPU graph widget.

---

## 7. Accessory Applets & System Tools

### 7.1 Sticky Notes (StikyNot.exe)
- **Visual Design:** Borderless, skeuomorphic post-it notes floating on the desktop.
- **Color Palettes:**
  - Yellow (Default): `#fef987`
  - Pink: `#fed8e7`
  - Green: `#d7fec7`
  - Blue: `#c7e8fe`
  - Purple: `#e6d7fe`
  - White: `#ffffff`
- **Header Bar:** Subtle top draggable margin revealing a `+` (New Note) button in top-left and `X` (Delete Note) in top-right on mouse hover.
- **Typography:** Segoe Print or Segoe Script handwriting font.

---

### 7.2 Windows Mobility Center (mblctr.exe)
- **Visual Design:** Grid of 8 distinct square cards set inside an Aero Glass dialog frame.
- **Tile Controls:**
  - Display Brightness slider.
  - Volume slider with mute checkbox.
  - Battery status indicator with Power Scheme dropdown.
  - Wireless Network toggle button (`Turn wireless on / off`).
  - External Display connection button.
  - Sync Center status card.
  - Presentation Settings toggle.

---

### 7.3 Windows Experience Index (WEI)
- **Base Score Badge:** Large rounded square with deep blue glass gradient, white bold score number (range `1.0` to `7.9`), and label "Base score".
- **Component Breakdown Table:**
  - Processor (Calculations per second).
  - Memory RAM (Memory operations per second).
  - Graphics (Desktop performance for Windows Aero).
  - Gaming Graphics (3D business and gaming graphics).
  - Primary Hard Disk (Disk data transfer rate).
  - Subscore badges aligned right.

---

### 7.4 Volume Mixer (SndVol.exe)
- Multi-channel vertical slider console partitioned into:
  - Device Master (Speakers / Headphones).
  - Applications (System Sounds, Web Browser, Media Player).
- Each channel contains: Application icon, volume slider, mute toggle button, and real-time vertical green LED peak meter.

---

### 7.5 Calculator (calc.exe)
- Completely overhauled in Windows 7 with mode switching:
  - Standard Mode.
  - Scientific Mode.
  - Programmer Mode: Hex, Dec, Oct, Bin base selectors, and a full 64-bit interactive bit-toggle matrix (clicking individual bit cells 0 to 63 toggles state).
  - Statistics Mode.

---

### 7.6 Snipping Tool
- Overlay Mode: Semi-transparent white screen wash (`rgba(255, 255, 255, 0.70)`) with transparent cutout over selected marquee region.
- Marquee Box: 2px solid red selection boundary.
- Floating toolbar with `New`, `Cancel`, and `Options` buttons.

---

### 7.7 The Windows Ribbon Framework (Scenic Ribbon / Navigation Ribbons)
Windows 7 debuted the Scenic Ribbon (Windows Ribbon Framework, `UIRibbon.h`), transitioning desktop applets from legacy 1990s Win32 menu-and-toolbar cascades into contemporary tabbed command bars.

- **Ribbon Layout & Geometry:**
  - **Quick Access Toolbar (QAT):** Embedded directly inside the top Aero Glass title bar (or toggled below the ribbon). Houses 16x16 icon action buttons (Save, Undo, Redo) followed by the customize dropdown chevron (`.ribbon-qat-dropdown`).
  - **Application Button (Backstage Pill):** Distinct 56x24px rectangular capsule anchored to the top-left corner of the ribbon. Features a high-gloss blue glass gradient (`#2b78c4` to `#15559c`), white text, and a white dropdown arrow. Triggers the primary application menu.
  - **Ribbon Tab Strip:** 24px horizontal tab row. Inactive tabs render as transparent pills with subtle light-blue hover glow. Active tab is solid white (`#ffffff`) with 1px border (`#abbcd1`) that merges seamlessly into the group container below.
  - **Ribbon Groups (Chunks):** 92px high main command container partitioned into discrete logical groups separated by 1px vertical borders (`#c2d5e3`). Each group includes:
    - Group Body: 68px command canvas hosting controls.
    - Group Caption Bar: 16px bottom strip with centered 9pt label in `#4c4c4c`.
    - Dialog Box Launcher (`.ribbon-dialog-launcher`): 14x14px square button in the bottom-right corner of the group caption featuring a diagonal arrow glyph (`-->`).
- **Ribbon Control Primitives:**
  - **Large Action Buttons (`.ribbon-btn-large`):** 32x32px icon centered above two lines of 9pt text inside a 42x66px touch target.
  - **Small Action Buttons (`.ribbon-btn-small`):** 16x16px icon button arranged in 3-row vertical stacks with optional adjacent label.
  - **Split Buttons (`.ribbon-split-btn`):** Split control where clicking the icon triggers default behavior, and clicking the dropdown arrow triggers a popover menu.
  - **In-Ribbon Galleries (`.ribbon-gallery`):** Horizontal scrollable grid of items flanked by up, down, and expand scroll buttons (`.ribbon-gallery-scroll`).
  - **Color Picker Matrix:** Dual active color swatches (Color 1 / Color 2) alongside a 2x10 grid of 16x16 color swatches.
  - **Zoom & Status Bar:** Bottom status strip hosting view modes and the continuous zoom slider (`-`, track with 100% notch, `+`, percentage readout).

---

### 7.8 WordPad (wordpad.exe)
Windows 7 completely replaced the legacy MFC/Win32 WordPad interface from Windows 95–Vista with a full Scenic Ribbon rich text authoring environment.

- **Ribbon Architecture:**
  - **Application Button:** Blue "WordPad" capsule button opening Backstage menu (New, Open, Save, Save As with RTF/DOCX/ODT/TXT sub-options, Print flyout with Quick Print and Print Preview, Page setup, Exit).
  - **Home Tab Chunks:**
    - `Clipboard`: Large Paste split button, Cut, Copy.
    - `Font`: Font Family combobox with typography preview, Font Size combobox, Grow font, Shrink font, Bold, Italic, Underline, Strikethrough, Subscript, Superscript, Text color picker split, Text highlight color. Dialog launcher opens the Font dialog.
    - `Paragraph`: Decrease indent, Increase indent, Start a list (Bullets, Numbered, Alphabetical), Line spacing (1.0, 1.15, 1.5, 2.0, Add 10pt space), Alignment (Left, Center, Right, Justify), Paragraph dialog launcher.
    - `Insert`: Picture split button, Paint drawing (embeds live paint session), Date and time, Insert object.
    - `Editing`: Find, Replace, Select all.
  - **View Tab Chunks:**
    - `Zoom`: Zoom in, Zoom out, 100% reset button.
    - `Show or hide`: Ruler checkbox, Status bar checkbox.
    - `Settings`: Word wrap options (No wrap, Wrap to window, Wrap to ruler), Measurement units (Inches, Centimeters, Points, Picas).
- **Authoring Surface & Interactive Ruler:**
  - **Ruler Bar (`.ruler`):** 18px horizontal strip positioned immediately below the ribbon. Displays inch/centimeter numeric intervals and tick marks with interactive draggable carats for First-line indent, Hanging indent, and Right margin.
  - **Document Canvas:** White document sheet (`#ffffff`) with subtle drop shadow centered on a light gray workspace backdrop (`#e8edf1`).
  - **Status Bar:** Bottom bar displaying page line count and the interactive zoom slider.

---

### 7.9 MS Paint (mspaint.exe)
MS Paint received its first comprehensive UI redesign in fifteen years with Windows 7, replacing the static 1995-era vertical tool strip with a modern Scenic Ribbon studio.

- **Ribbon Architecture:**
  - **Application Button:** Blue "Paint" capsule button opening the file menu (New, Open, Save, Save As with PNG/JPEG/BMP/GIF flyouts, Print flyout, From scanner or camera, Set as desktop background, Properties, Exit).
  - **Home Tab Chunks:**
    - `Clipboard`: Paste split button, Cut, Copy.
    - `Image`: Select split button (Rectangular selection, Free-form selection, Select all, Invert selection, Delete, Transparent selection toggle), Crop button, Resize and Skew dialog trigger, Rotate dropdown (Rotate right 90°, Rotate left 90°, Rotate 180°, Flip vertical, Flip horizontal).
    - `Tools`: Pencil, Fill with color (paint bucket), Text (`A`), Eraser, Color picker (eyedropper), Magnifier.
    - `Brushes`: Large split button with dropdown preview of 9 artistic brush engines (Calligraphy brush 1, Calligraphy brush 2, Airbrush, Oil brush, Crayon, Marker, Natural pencil, Watercolor brush).
    - `Shapes`: In-ribbon scrollable gallery displaying 23 vector shapes (Lines, Ovals, Rectangles, Rounded rectangles, Polygons, Triangles, Arrows, Stars, Callout speech bubbles, Heart, Lightning), accompanied by Outline and Fill style dropdowns.
    - `Size`: Stroke width picker displaying 1px, 2px, 3px, and 4px line options.
    - `Colors`: Foreground (Color 1), Background (Color 2), 20-swatch palette grid (2 rows of 10), and "Edit colors" button launching the 48-color picker modal.
  - **View Tab Chunks:**
    - `Zoom`: Zoom in, Zoom out, 100% reset.
    - `Show or hide`: Rulers, Gridlines, Status bar checkboxes.
    - `Display`: Full screen, Thumbnail preview window.
- **Drawing Canvas & Status Telemetry:**
  - White bitmap drawing canvas featuring 8 discrete square resize handles (corners and midpoints).
  - Status bar tracking live pointer coordinates (`X, Y px`), selection marquee dimensions (`W x H px`), total canvas resolution (`1024 x 768px`), and zoom slider.

---

### 7.10 Resource Monitor (resmon.exe) & XP-to-7 System Overhauls
Beyond WordPad and Paint, Windows 7 replaced several rudimentary Windows XP utility windows with high-density telemetry dashboards:

- **Resource Monitor (`resmon.exe`):**
  - Replaced the basic XP Performance tab with a 5-tab real-time monitoring console (`Overview`, `CPU`, `Memory`, `Disk`, `Network`).
  - Table Accordions: Collapsible gradient section headers displaying active metrics, error rates, and checkbox process filtering.
  - Live Telemetry Sparklines: Right-hand sidebar hosting real-time scrolling SVG/Canvas sparklines for CPU (Total & per-core), Disk I/O, Network transfer, and Physical Memory allocation.
- **Device Stage (Devices and Printers):**
  - Replaced XP's plain list with photorealistic 3D hardware cards showing printer ink levels, scanner status, and connected peripherals.

---

## 8. Media Experiences & Motion Mechanics

### 8.1 Windows Media Player 12 (WMP 12)
- **Now Playing Mode:** Floating borderless window with dark smoky glass backdrop, album art card, seek bar, and translucent circular blue transport buttons.
- **Taskbar Deskband Player:** Minimizing WMP embeds a mini player directly into the taskbar thumbnail preview with interactive playback controls.

---

### 8.2 Shell Motion & Window Mechanics
- **Aero Snap Overlay:** Semi-transparent light-blue docking preview rectangle appearing when dragging a window to screen perimeters.
- **Aero Shake:** Rapid mouse shaking of an active title bar minimizes all background windows.
- **Aero Peek Wireframes:** Inactive windows render as translucent 1px white border silhouettes with clear glass bodies when peaking.
- **Blue Screen of Death (BSOD):** Classic solid blue `#000082` crash screen with white monospace `Lucida Console` diagnostic text, prior to modern graphical restart screens.

---

## 9. Architectural Allocation Matrix

| Component Group | Specific UI Elements | Library Tier | Implementation Target |
| :--- | :--- | :--- | :--- |
| **Form Controls** | Buttons, Checkboxes, Radios, Sliders, Spinners, Text inputs, Progress bars | Core CSS | `gui/*.scss` |
| **Command Primitives** | Command Links, Split Buttons, Breadcrumb Bars, Search Inputs | Core CSS | `gui/*.scss` |
| **Navigation Ribbons** | Quick Access Toolbar, Application Button, Ribbon Tabs, Chunks, Dialog Launchers, Galleries | Core CSS | `gui/*.scss` |
| **Structural Containers** | Window Frames, Task Dialogs, Property Sheets, Action Panes, Splitters, Rulers | Core CSS | `gui/*.scss` |
| **Shell Widgets** | Start Orb, Superbar Tiles, Desktop Gadget Bezels, Status Bars, Infobars, ScreenTips | Core CSS | `gui/*.scss` |
| **System Tool Elements** | Sticky Notes cards, WEI Score Badges, CPU Sparkline Grids, Bit-toggle matrix, Zoom slider | Core CSS | `gui/*.scss` |
| **Composite Consoles** | Event Viewer (MMC 3.0), Control Panel, Task Manager, Volume Mixer, Resource Monitor | Showcase Layouts | `examples/*.html` and `docs/` |
| **Ribbon Applets** | WordPad 7 rich text editor, MS Paint 7 graphics studio | Showcase Layouts | `examples/*.html` and `docs/` |
| **Full Desktop Surface** | Desktop Canvas with taskbar, start menu, floating gadgets, and logon lock screen | Showcase Layouts | `examples/*.html` |
| **Audio Engine** | Web Audio API sound triggers for clicks, navigation, balloons, errors | Optional Script | `dist/7.audio.js` |
| **Companion / Assistant** | Clippy or agent avatar | Out of Core Scope | Optional Portfolio Add-on |
