# dekcx Theme Notes

Source analyzed from a live Habbo archive deployment (read-only):
- CSS layout and palette sources
- header and footer interaction scripts
- core content templates and archive pages

## Core Visual System
- Primary background: near-black navy (`#06060f`) with subtle dot-grid texture.
- Panel/surface hierarchy:
  - panel: `#0d1117`
  - window: `#111827`
  - raised: `#1a2035`
- Accent: Habbo orange (`#FF9900`) with glow.
- Secondary blue for framing (`#4a8fcc` family).
- Typography: Verdana body; Goldfish/Volter-style pixel font for brand and key counters.
- Borders are sharp and squared (`0px` radius) with hard 2px strokes.
- Shadows are hard offset, not soft blur (`4px 4px 0 rgba(0,0,0,.6)`).

## Header Pattern
- Dark panel header with orange bottom border and subtle shadow line.
- Left brand block with icon + uppercase logo treatment + subtitle.
- Center tab-like nav with active state filled by orange.
- Right utility/counter area.

## Main Content Pattern
- Modular window cards with titlebar/chrome feel.
- Strong bordered cards with hover border-to-accent transition.
- Search/tool rows use high-contrast framed inputs.
- Badge chips are small, uppercase, and square.

## Footer Pattern
- Utility footer with many compact link buttons.
- Button style is framed/square and accent-on-hover.
- Author/identity is present but minimal.

## dChat Translation Decisions
- Added optional `theme_preset=dekcx`.
- Preset keeps full color token editability (`accent/bg/surface/text/muted/link/radius`).
- Added dedicated `theme-dekcx.css` for structural mimic:
  - header/nav treatment
  - card borders/shadows
  - compact uppercase controls
  - footer link button styling
  - Habbo-like visual density and contrast
