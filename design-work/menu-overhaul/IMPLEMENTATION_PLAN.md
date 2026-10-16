# ArcaneBeam Menu Overhaul Implementation Plan

Target design: **Option B - Arcane Starforge Hybrid**

Primary goal: keep the live world preview readable while editing every ability tab.

## Status

- [x] Pick layout direction: collapsible bottom drawer
- [x] Pick theme direction: Arcane Starforge Hybrid
- [x] Generate layout mockups
- [x] Generate theme comparison mockups
- [x] Generate 9-slice atlas preview
- [x] Implement GUI atlas and 9-slice renderer
- [x] Replace current full-screen config layout
- [x] Add Clean View restore handle
- [x] Polish dense color-label placement
- [x] Build and verify release jar

## Implementation Pass 1 - 2026-06-21

- [x] Added production GUI atlas at `src/main/resources/assets/arcanebeam/textures/gui/config_atlas.png`
- [x] Added procedural atlas generator at `design-work/menu-overhaul/generate_config_atlas.py`
- [x] Added `NineSliceRenderer`
- [x] Added `ArcaneBeamGuiTheme`
- [x] Removed full-screen `renderBackground()` from the config screen render path
- [x] Added top ability tab bar chrome
- [x] Added expanded bottom drawer chrome
- [x] Added collapsed drawer handle
- [x] Added `Clean View` button and `H` restore/hide hotkey
- [x] Moved existing controls into drawer/card coordinates without changing config save/load behavior
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass at multiple GUI scales
- [x] Data-driven tab descriptor refactor
- [x] Overflow scrolling for future extra tabs
- [x] True color picker popover
- [x] Full custom themed rendering for buttons, edit boxes, and sliders
- [x] Bottom overflow and input text alignment polish

## Implementation Pass 2 - 2026-06-21

- [x] Fixed cramped first-pass layout from in-game screenshots
- [x] Gave top bar a dedicated brand area so title and tabs no longer overlap
- [x] Reworked collapsed drawer so text and buttons no longer overlap
- [x] Split drawer into non-overlapping profile, color, and control card zones
- [x] Moved the palette out of the drawer into an on-demand popover
- [x] Added `ConfigTabId` and tab descriptors for current tabs
- [x] Added overflow-aware top tab layout with left/right arrows
- [x] Added mouse-wheel horizontal tab scrolling
- [x] Added active-tab auto-scroll
- [x] Added themed button rendering
- [x] Added themed slider rendering
- [x] Added 9-slice frames behind edit boxes
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after cramped-layout correction
- [ ] Semantic per-setting card descriptors for every Phase 6 card

## Implementation Pass 3 - 2026-06-21

- [x] Increased expanded drawer height from `312` to `364` virtual pixels
- [x] Tightened Arcane/Rail row spacing so sound, transition, and origin controls stay inside the bottom drawer
- [x] Tightened Lightning Strike row spacing so lifetime, sides, ripple, delay, and volume fields stay inside the control card
- [x] Tightened Vault Altar row spacing so origin marker and volume controls stay inside the control card
- [x] Tightened Storm Arrow/Smite/Archon row spacing so lifetime, height, audio range, missile radius, and volume controls stay inside the control card
- [x] Retained native `EditBox` bordered text layout so input text is vertically centered by Minecraft's built-in renderer
- [x] Resized 9-slice input frames to match bordered `EditBox` inner widths
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after bottom-overflow correction

## Implementation Pass 4 - 2026-06-21

- [x] Renamed `Hide UI` to `Clean View` to clarify the mode
- [x] Made `Clean View` hide ArcaneBeam chrome and suppress vanilla/Forge/Vault HUD overlays
- [x] Temporarily sets `Minecraft.options.hideGui = true` while clean preview is active
- [x] Cancels `RenderGameOverlayEvent.Pre` for `ElementType.ALL` while clean preview is active
- [x] Restores the player's previous `hideGui` state when `H` restores the menu or the screen closes
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after HUD suppression correction

## Implementation Pass 5 - 2026-06-21

- [x] Reviewed current state screenshots across Arcane, Rail, Lightning Strike, Vault Altar, Storm Arrow, Smite, Archon, and color picker
- [x] Suppressed vanilla/Forge/Vault HUD overlays for the full config-screen lifetime, not only `Clean View`
- [x] Kept `Clean View` focused on hiding ArcaneBeam chrome while preserving restore-to-collapsed/expanded state
- [x] Moved slider labels above the track/handle to remove handle/text collisions
- [x] Added compact slider labels for narrow dense-tab controls
- [x] Removed redundant Arcane/Rail `Ticks` labels that collided visually with transition buttons
- [x] Shortened the color picker helper caption so it no longer clips
- [x] Removed the extra `Shockwave` row label that protruded outside the Lightning color card
- [x] Updated drawer hint text to reference `Clean View`
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after dense-slider readability correction

## Implementation Pass 6 - 2026-06-21

- [x] Added a bottom-center 9-slice `Restore Menu (H)` handle while `Clean View` is active
- [x] Made the restore handle clickable so the menu can return without closing/reopening the screen
- [x] Kept `H` as the keyboard restore/hide shortcut when no text input is focused
- [x] Removed redundant dense color-card row titles that competed with slot labels
- [x] Moved Lightning Strike, Vault Altar, Storm Arrow, Smite, and Archon color-slot labels above each swatch/hex group
- [x] Updated README, project memory, and version memory for the current Clean View behavior
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after Clean View restore/color-label polish

## Implementation Pass 7 - 2026-06-21

- [x] Reviewed current screenshots with red-arrow concerns
- [x] Initially shifted Arcane/Rail color rows right so `Beam` and `Glow` labels sat in a readable inner gutter before the later universal row-format pass
- [x] Kept dense-tab color row alignment unchanged
- [x] Reduced the color picker inset frame width so the right edge no longer protrudes past the popover panel
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after Arcane/Rail label-gutter iteration and color-picker frame correction

## Implementation Pass 8 - 2026-06-21

- [x] Added semantic section chips above dense-tab control columns
- [x] Added per-tab dense section labels for Lightning Strike, Vault Altar, Storm Arrow, Smite, and Archon
- [x] Added an Arcane/Rail `Control Groups` legend in the unused right side of the control card when enough width is available
- [x] Kept all widgets in their current positions and preserved existing config save/load behavior
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after semantic section-guide overlay

## Implementation Pass 9 - 2026-06-21

- [x] Added a dedicated hex input row inside the color picker popover
- [x] Synced the popover hex input with the currently selected color slot
- [x] Routed popover hex edits through the existing selected-color setter so all tabs keep their current color behavior
- [x] Hid and unfocused the popover hex input when the picker closes, drawer collapses, tab changes, or Clean View opens
- [x] Kept `H` from toggling Clean View while the popover hex input is focused
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after color-picker hex input

## Implementation Pass 10 - 2026-06-21

- [x] Added lightweight sub-card backgrounds behind existing control groups
- [x] Added dense-tab column sub-card backgrounds
- [x] Added Arcane/Rail sub-card backgrounds for Shape, Motion, Advanced, Audio, Transition, and Origin control bands
- [x] Kept widget positions and config behavior unchanged
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after Phase 5 sub-card backgrounds

## Implementation Pass 11 - 2026-06-21

- [x] Added horizontal scroll state for overflowing control-card content
- [x] Reset control scroll position on tab changes
- [x] Added mouse-wheel scrolling over the control-card viewport
- [x] Added dense-tab column snapping for normal wheel movement
- [x] Added a subtle control-card scrollbar/overflow hint
- [x] Made off-viewport control widgets and labels inactive/hidden so they do not render outside the drawer
- [x] Centralized beam and dense control widths for consistent card stretching
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after control-card overflow scrolling

## Implementation Pass 12 - 2026-06-21

- [x] Converted Arcane/Rail control widgets into horizontal Phase 6 cards
- [x] Added titled Shape, Motion, Advanced, Audio, Transition, and Origin cards for Arcane/Rail
- [x] Moved the Arcane/Rail sound-volume input onto a second Audio-card row to avoid label/button collisions
- [x] Added Beam Colors and Glow Colors subcards inside the Arcane/Rail Colors card
- [x] Removed the redundant Arcane/Rail color caption that overlapped the new color subcards
- [x] Preserved existing config responders and save/load behavior
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after Arcane/Rail Phase 6 card conversion

## Implementation Pass 13 - 2026-06-21

- [x] Converted Lightning Strike controls into Setup, Shockwave, Opacity, Center Geometry, Spots, Ripples, and Audio cards
- [x] Converted Vault Altar controls into Setup, Corner Beam, Center Beam, Glow, Origin, Timing, and Audio cards
- [x] Converted Storm Arrow controls into Setup, Targeting, Projectile, Strike, Impact, and Audio cards
- [x] Converted Smite controls into Setup, Targeting, Strike, Activation, Impact, and Audio Range cards
- [x] Converted Archon controls into Setup, Targeting, Missile, Strike + Impact, Activation, Strike Audio, and Audio Range cards
- [x] Kept dense-tab color swatches in the dedicated Colors card with their existing labels and picker behavior
- [x] Restored the Segment Gap slider inside Storm Arrow/Smite Strike cards now that the card layout has room for it
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after dense-tab Phase 6 card conversion

## Implementation Pass 14 - 2026-06-21

- [x] Reduced expanded drawer height from `364` to `264` virtual pixels so the live preview has more vertical space
- [x] Balanced Arcane/Rail Colors and Beam Controls card widths on wide screens
- [x] Kept a `430` pixel minimum for Arcane/Rail Colors so color rows do not crush on small screens
- [x] Left dense-tab Colors width fixed because their Effect Controls card benefits more from the extra horizontal viewport
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after compact drawer and Arcane/Rail width balance

## Implementation Pass 15 - 2026-06-21

- [x] Removed redundant Arcane/Rail left-side `Beam` and `Glow` row labels from the Colors card
- [x] Centered Arcane/Rail color rows inside the Colors card for a more universal swatch/input format
- [x] Initially kept `Beam Colors` and `Glow Colors` subcard titles as the group labels before the later universal slot-label pass
- [x] Removed the unused row-label gutter constant from `ArcaneBeamConfigScreen`
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after universal Arcane/Rail color-row format

## Implementation Pass 16 - 2026-06-21

- [x] Made the Colors card width fixed and universal across Arcane, Rail, and dense tabs
- [x] Removed the special Arcane/Rail `Beam Colors` and `Glow Colors` color-row subcard chrome
- [x] Switched Arcane/Rail to the same label-above-slot format as other tabs using `Core 1-4` and `Glow 1-4`
- [x] Changed control-card wheel scrolling to snap to actual card boundaries
- [x] Initially hid controls unless their parent card was visible enough to avoid orphaned inputs at scroll edges
- [x] Removed stale semantic-guide helper code that was superseded by titled control cards
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after universal Colors width and card-boundary scrolling

## Implementation Pass 17 - 2026-06-21

- [x] Kept partially visible control-card chrome rendered at scroll edges to avoid big blank gutters
- [x] Limited control-card title chips to fully visible positions so text is not clipped at the viewport edge
- [x] Kept buttons, inputs, sliders, and manual labels hidden only when the widget itself would clip outside the control viewport
- [x] Removed the parent-card-full-visibility gate from control widget visibility
- [x] Ran `bash ./gradlew build`
- [ ] In-game visual pass after scroll-edge chrome/child visibility correction

## Source Mockups

- [Contact sheet](mockups/menu_overhaul_contact_sheet.png)
- [Option B base mockup](mockups/option_b_bottom_drawer.png)
- [Theme comparison](mockups/option_b_theme_comparison.png)
- [Recommended hybrid theme](mockups/theme_arcane_starforge_hybrid.png)
- [9-slice atlas preview](mockups/nine_slice_atlas_preview.png)

## Phase 1 - GUI Foundation

- [x] Add `src/main/resources/assets/arcanebeam/textures/gui/config_atlas.png`
- [x] Add a `NineSliceRenderer` helper
- [x] Define atlas regions for:
  - [x] `glass_panel`
  - [x] `iron_panel`
  - [x] `gold_drawer`
  - [x] `button`
  - [x] `color_slot`
- [x] Add a `ConfigTheme` helper for:
  - [x] panel colors
  - [x] tab accent colors
  - [x] drawer chrome colors
  - [x] text colors
  - [x] selected/hover/disabled states
- [x] Stop using full-screen `renderBackground()` in `ArcaneBeamConfigScreen`
- [x] Draw only localized translucent backgrounds behind top bar, drawer, popovers, and dropdowns
- [ ] Verify the live world preview remains visible behind the menu
- [x] Override `isPauseScreen()` if needed so previews remain live in singleplayer

## Phase 2 - Data-Driven Tabs

- [x] Add `ConfigTabId`
- [x] Replace hardcoded tab booleans with one active tab id
- [ ] Create a tab descriptor structure with:
  - [x] id
  - [x] label
  - [x] accent color
  - [ ] category
  - [ ] drawer card list
  - [ ] preview mode
- [ ] Register current tabs:
  - [x] Arcane
  - [x] Rail
  - [x] Lightning Strike
  - [x] Vault Altar
  - [x] Storm Arrow
  - [x] Smite
  - [x] Archon
- [x] Keep current config save/load behavior unchanged

## Phase 3 - Future-Proof Tab Overflow

- [x] Implement top tab bar layout from the tab descriptor list
- [x] Show all tabs when they fit
- [x] Add left/right arrows when tabs overflow
- [x] Add mouse-wheel horizontal scrolling over the tab bar
- [x] Auto-scroll the active tab into view
- [ ] Leave room for a future `More` dropdown if the tab count grows beyond roughly 10 tabs
- [ ] Test with temporary extra dummy tabs during development

## Phase 4 - Bottom Drawer Shell

- [x] Add drawer state enum:
  - [x] `EXPANDED`
  - [x] `COLLAPSED`
  - [x] `HIDDEN`
- [x] Draw the expanded 9-slice bottom drawer
- [x] Draw the collapsed bottom handle
- [x] Add `Collapse` button
- [x] Add `Clean View` button or hotkey while the screen is open
- [x] Keep `Esc` as normal close behavior
- [x] Reserve a center preview safe zone above the drawer
- [ ] Ensure the drawer scales cleanly at small resolutions and large GUI scale

## Phase 5 - Card-Based Drawer Layout

- [x] Add a card descriptor or card rendering abstraction
- [x] Support common card types:
  - [x] Profile
  - [x] Colors
  - [x] Shape
  - [x] Beam
  - [x] Motion
  - [x] Audio
  - [x] Advanced
- [x] Lay cards horizontally in the drawer
- [x] Add horizontal card scrolling if cards overflow
- [x] Keep card widths consistent enough for 9-slice stretching

## Phase 6 - Move Current Controls Into Cards

### Arcane

- [x] Profile card
- [x] Beam color card
- [x] Glow color card
- [x] Beam shape card: intensity, opacity, glow radius, glow opacity
- [x] Motion card: color shift, glow rotation
- [x] Transition card: fade/grow in, fade/shrink out, ticks
- [x] Origin card: hand, X/Y/Z offsets
- [x] Audio card: sound choice, volume
- [x] Shader compatibility control

### Rail

- [x] Profile card
- [x] Beam color card
- [x] Glow color card
- [x] Beam shape card
- [x] Motion card
- [x] Transition card
- [x] Origin card
- [x] Audio card
- [x] Shader compatibility control

### Lightning Strike

- [x] Profile card
- [x] Enable/shader/fullbright controls
- [x] Shockwave shape card: start radius, end radius, edge width, side count
- [x] Opacity card: alpha, interior opacity
- [x] Center geometry card: sphere radius/opacity, cone height/width/opacity
- [x] Spots card: count, size, opacity
- [x] Ripples card: secondary count, size, delay
- [x] Audio card: sound mode, volume

### Vault Altar

- [x] Profile card
- [x] Enable/shader/fullbright controls
- [x] Corner beam card: colors, radius, opacity, vertical ticks, converge ticks
- [x] Origin card: origin height, origin radius, origin markers
- [x] Center beam card: colors, height, fade height, bottom/top radius, opacity
- [x] Glow card: colors, height, fade height, bottom/top radius, opacity, rotation
- [x] Timing card: center grow ticks
- [x] Audio card: sound mode, volume

### Storm Arrow

- [x] Profile card
- [x] Enable/shader/fullbright controls
- [x] Targeting circle card: show, actual radius, color, alpha, thickness
- [x] Projectile card: projectile sound mode, audio range
- [x] Strike card: blaster color, core color, alpha, width, segment length, segment gap
- [x] Impact card: flash enabled, flash color, flash size, lifetime, origin height
- [x] Audio card: strike sound mode, volume

### Smite

- [x] Profile card
- [x] Enable/shader/fullbright controls
- [x] Targeting circle card
- [x] Strike card
- [x] Activation audio card
- [x] Impact card
- [x] Audio range control

### Archon

- [x] Profile card
- [x] Enable/shader/fullbright controls
- [x] Targeting circle card
- [x] Missile card: missile origin radius, origin height, segment length
- [x] Strike/impact card
- [x] Activation audio card
- [x] Strike audio card
- [x] Audio range control

## Phase 7 - Color Picker Popover

- [x] Replace always-visible palette with a popover
- [x] Open popover when a color chip is clicked
- [x] Draw palette in a 9-slice panel above the drawer
- [x] Draw brightness strip inside the popover
- [x] Keep hex input in the popover
- [x] Support drag updates for palette and brightness
- [x] Close popover by clicking outside, pressing Escape once, or selecting another chip
- [x] Keep the preview visible while the popover is open

## Phase 8 - Themed Widgets

- [x] Draw 9-slice frames behind vanilla `EditBox` widgets
- [x] Make `EditBox` borders invisible or visually neutral where possible
- [x] Replace vanilla button rendering with themed button rendering
- [x] Replace slider rendering with Arcane Starforge slider styling
- [x] Add hover and focus states
- [x] Add active-tab glow
- [-] Add subtle glyph corner marks without copying any third-party UI symbols(skip until mentioned)

## Phase 9 - Verification

- [ ] Verify at `1280x720`
- [ ] Verify at `1920x1080`
- [ ] Verify at high GUI scale
- [ ] Verify at small GUI scale
- [ ] Verify with drawer expanded
- [ ] Verify with drawer collapsed
- [ ] Verify with drawer hidden
- [ ] Verify with profile dropdown open
- [ ] Verify with color picker open
- [ ] Verify every current tab
- [ ] Verify profile add/select/save still works
- [ ] Verify existing config migration still works
- [ ] Verify live preview remains visible
- [ ] Run build:

```bash
bash ./gradlew build
```

## Implementation Notes

- Do not rewrite ability behavior while changing the menu.
- Keep config schema unchanged unless a specific UI state needs persistence.
- Keep the first implementation conservative: move existing controls before replacing every widget renderer.
- If the drawer gets too crowded, prefer horizontal card scrolling over increasing drawer height.
- Do not use direct Star Wars branding, logos, exact Aurebesh, or copied UI shapes. The target is original arcane sci-fi.
