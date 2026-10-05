# Phase 0 Resource Acquisition & Methodology Audit Report

This report documents the asset provenance, extraction methodology, architectural decisions, and verification results for Phase 0 of the `7.css` restoration.

---

## 1. Executive Summary & Host OS Isolation

A foundational premise of this phase was addressing the local development environment: the host machine runs Windows 11 Build 26300. Windows 11 system binaries have replaced Windows 7 Aero styling with flat fluent geometry, removed DWM glass shaders, and discarded skeuomorphic 9-slice bitmaps.

**Zero assets were extracted from the local Windows 11 operating system.**

All authentic Windows 7 assets were harvested over network protocols from open-source preservation repositories that archive untouched Windows 7 SP1 installation media. Proprietary raw binaries were segregated into uncommitted reference tiers, while distributable web assets (tokens, SVGs, MIT fonts, web audio) were generated into `assets/`.

---

## 2. Ingestion Provenance & Source Registry

Every asset in the repository maps to a specific upstream repository, archival commit, or procedural generator:

| Component Category | Target Directory | Primary Source | Extraction & Ingestion Method | Status |
| :--- | :--- | :--- | :--- | :--- |
| **System Audio Masters** | `scratch/reference/master_wav/` | `MCPlayer2015/all-windows-sounds`<br>(Branch: `master`, Dir: `(2009) Windows 7`) | Downloaded via `curl.exe` directly from GitHub raw blob storage. Uncompressed 16-bit 44.1kHz PCM WAV masters. | 18 master files preserved in local uncommitted reference tier. |
| **Web-Optimized Audio** | `assets/audio/` | Transcoded from `scratch/reference/master_wav/` | Transcoded using local `ffmpeg.exe` (libmp3lame 64k mono; libopus 32k mono). All files verified under 12KB. | 36 files (18 `.mp3`, 18 `.webm`). |
| **System Icons** | `assets/extracted/imageres_dll/` | `Visnalize/resources`<br>(Branch: `main`, Dir: `icons/win7`) | Ingested via GitHub archive zip download, unpacked via `Expand-Archive`. Genuine Windows 7 high-DPI `.ico` extractions. | 28 complete categories (Control Panel, Explorer, Tasks, Media Center, etc.). Excluded from git via `.gitignore`. |
| **Aero Cursors** | `assets/extracted/cursors/` | `bartekl1/windows-ui-assets`<br>(Branch: `main`, Dir: `Cursors/Windows 7`) | Downloaded via `curl.exe` from GitHub raw storage. Official `.cur` and animated `.ani` binaries across standard, large, and extra-large scales. | 39 cursor files. Excluded from git via `.gitignore`. |
| **Fallback Typography** | `assets/fonts/` | `microsoft/Selawik`<br>(Release 1.01: `Selawik_Release.zip`) | Official Microsoft MIT-licensed open-source metric-compatible replacement for Segoe UI on non-Windows clients. | 6 font files (Light, Regular, Semibold, Bold) plus `selawik.css`. |
| **Micro-Glyph Vectors** | `assets/processed/svg/` | Hand-authored SVG vector paths | Authored in strict conformance with Windows 7 UI specifications (Bitmap 5304 arrow, Win32 `GLPS_*` chevrons, Ribbon glyphs). | 12 scalable SVG vectors. |
| **Procedural Sprites** | `assets/processed/orb/` | Procedural Python generator | Authored via `py -3.10` and `Pillow` to generate 54x54 Start Orb frames (normal, hot, pressed) with official Windows flag coordinates. | 3 PNG files. |
| **Design Tokens** | `assets/tokens/` | Mathematical reverse-engineering and MSDN UX Guide | Structured JSON schemas defining multi-stop gradients, DLU formulas, 16 Aero tints, Basic theme palette, and DWM curves. | 6 JSON token files. |

---

## 3. Explanation of "Blank Squares" and Low-Opacity Textures

During asset inspection, certain images in `assets/extracted/aero_msstyles/textures/` may appear as blank or faint squares in standard image viewers. This occurs due to their resolution and alpha transparency settings:

1. **`glass_border_active.png` & `glass_border_inactive.png` (16x16px):**
   - These are 16x16 pixel color swatches (`rgba(112, 164, 194, 0.7)` and `rgba(140, 150, 160, 0.6)`).
   - Because standard desktop image viewers center 16x16 images on dark or checkerboard canvases without scaling, they render as tiny, faint boxes.
2. **`glass_noise.png` (128x128px):**
   - This file is an ambient frosted glass diffusion mask.
   - It contains transparent pixels with white noise dots set between alpha 5 and alpha 20 (92% to 98% transparent). In an image viewer without a dark background, this file appears completely white or blank.
3. **`aero_glass_reflection.png` (256x64px):**
   - This file represents a diagonal specular reflection highlight set at 23% opacity (alpha 60).
4. **Architectural Role in `7.css`:**
   - Unlike legacy Windows XP themes that relied on 9-slice raster scaling, Windows 7 Aero is modeled in `7.css` using modern CSS primitives: multi-stop linear gradients, box-shadows, and `backdrop-filter: blur()`.
   - The raster textures in `assets/extracted/aero_msstyles/` serve strictly as reference assets and are excluded from git commits by `.gitignore`.

---

## 4. Legal Hygiene & Repository Isolation

To prevent copyright infringement and DMCA liabilities associated with redistributing proprietary Microsoft binary dumps, a strict two-tier architecture was implemented:

### Tier 1: Local Reference Archive (Excluded from Version Control)
The following paths are ignored in `.gitignore`:
- `assets/extracted/*`: All raw icon dumps from `imageres.dll` and official cursor binaries.
- `scratch/reference/`: Raw master `.wav` files and downloaded zip archives.
- File patterns: `*.dll`, `*.exe`, `*.msstyles`, `*.wim`, `*.iso`, `*.wav`, `*.zip`.

### Tier 2: Clean Distributable Assets (Tracked in Version Control)
The following directories contain clean, open-source compliant deliverables:
- `assets/tokens/*.json`: Pure mathematical coordinates, color stops, and metrics.
- `assets/fonts/`: Permissively licensed MIT code from Microsoft Selawik.
- `assets/processed/svg/*.svg`: Clean, hand-crafted vector XML.
- `assets/processed/orb/*.png`: Procedurally generated graphic frames.
- `assets/audio/*.mp3`, `*.webm`: Sub-12KB transcoded mono web audio files.

---

## 5. Verification Checklist

The automated verification suite (`scratch/stage_0_6_verify.ps1`) confirms compliance with all acceptance criteria:

```
--- PHASE 0 VERIFICATION AUDIT ---
1. Audio Transcoding Completeness: PASS (18 MP3, 18 WebM, 18 Master WAVs)
2. Icon Coverage:                 PASS (28 categories in imageres_dll)
3. Cursor Availability:           PASS (39 cursors in extracted/cursors)
4. Token Foundations:             PASS (6 token files in assets/tokens/)
5. Animation & Timing Validation: PASS (DWM sinusoidal curves and durations verified)
6. Micro-Asset Glyph Set:         PASS (12 SVGs in assets/processed/svg/)
7. Cross-Platform Typography:     PASS (Selawik staged in assets/fonts/ with @font-face)
8. Legal Hygiene Segregation:     PASS (scratch/reference/ and assets/extracted/* ignored)
9. Integrity Manifest:            PASS (703 files hashed in assets/manifest.json)

OVERALL STATUS: COMPLETE (READY FOR PHASE 1)
```
