# ArcaneBeam Menu Overhaul Mockups

Generated mockups for replacing the current full-foreground config screen with preview-first layouts.

## Current Constraint

`ArcaneBeamConfigScreen.render` calls `renderBackground`, then renders all widgets over a scaled virtual layout. This makes the world-space preview hard to read because the whole screen is dimmed and the controls sit in the preview area.

## Options

### A. Side Inspector

File: `mockups/option_a_side_inspector.png`

- Left vertical ability rail.
- Right 9-slice inspector panel for the active ability settings.
- Center/left preview safe zone stays mostly uncovered.
- Lowest-risk implementation because it maps cleanly to existing settings groups.

Recommended when: we want a practical redesign quickly.

### B. Collapsible Bottom Drawer

File: `mockups/option_b_bottom_drawer.png`

- Full-width preview remains visible above the controls.
- Controls live in a bottom drawer that can collapse to a short handle.
- Strong fit for Lightning Strike, Vault Altar, Storm Arrow, Smite, and Archon because those effects use center-screen/world-space previews.

Recommended when: preview visibility is the top priority.

### C. Floating Toolcards

File: `mockups/option_c_floating_toolcards.png`

- Active controls open as small cards around screen edges.
- Center remains almost completely unobstructed.
- More immersive, but needs more custom widget/state work.

Recommended when: we want the most polished long-term UX.

## 9-Slice Support

File: `mockups/nine_slice_atlas_preview.png`

Proposed atlas regions:

- `glass_panel`: translucent editor cards.
- `iron_panel`: neutral panels and inactive sections.
- `gold_drawer`: highlighted drawer/header chrome.
- `button`: buttons, active tabs, dropdown rows.
- `color_slot`: color swatches and small value cells.

Suggested implementation path:

1. Add `assets/arcanebeam/textures/gui/config_atlas.png`.
2. Add a small Java helper that draws 9-slice regions with `GuiComponent.blit`.
3. Replace full-screen `renderBackground` with localized dimming only behind panels.
4. Keep `EditBox` text input initially, but draw 9-slice frames behind it.
5. Convert sliders/buttons/tabs to custom renderers after the layout is stable.
6. Add a `hideChrome` or `collapsed` state so the preview can be inspected without closing the screen.

## Recommendation

Start with Option B if preview visibility is the highest priority. Start with Option A if implementation speed and low regression risk matter more.
