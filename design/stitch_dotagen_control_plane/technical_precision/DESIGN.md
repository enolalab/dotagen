---
name: Technical Precision
colors:
  surface: '#131315'
  surface-dim: '#131315'
  surface-bright: '#39393b'
  surface-container-lowest: '#0e0e10'
  surface-container-low: '#1c1b1d'
  surface-container: '#201f22'
  surface-container-high: '#2a2a2c'
  surface-container-highest: '#353437'
  on-surface: '#e5e1e4'
  on-surface-variant: '#c4c7c8'
  inverse-surface: '#e5e1e4'
  inverse-on-surface: '#313032'
  outline: '#8e9192'
  outline-variant: '#444748'
  surface-tint: '#c6c6c7'
  primary: '#ffffff'
  on-primary: '#2f3131'
  primary-container: '#e2e2e2'
  on-primary-container: '#636565'
  inverse-primary: '#5d5f5f'
  secondary: '#c8c6c9'
  on-secondary: '#303033'
  secondary-container: '#47464a'
  on-secondary-container: '#b6b4b8'
  tertiary: '#ffffff'
  on-tertiary: '#32302d'
  tertiary-container: '#e7e1dd'
  on-tertiary-container: '#676460'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e2e2e2'
  primary-fixed-dim: '#c6c6c7'
  on-primary-fixed: '#1a1c1c'
  on-primary-fixed-variant: '#454747'
  secondary-fixed: '#e4e1e5'
  secondary-fixed-dim: '#c8c6c9'
  on-secondary-fixed: '#1b1b1e'
  on-secondary-fixed-variant: '#47464a'
  tertiary-fixed: '#e7e1dd'
  tertiary-fixed-dim: '#cbc6c1'
  on-tertiary-fixed: '#1d1b19'
  on-tertiary-fixed-variant: '#494643'
  background: '#131315'
  on-background: '#e5e1e4'
  surface-variant: '#353437'
typography:
  display:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline:
    fontFamily: Geist
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-base:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Geist
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  mono-base:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  mono-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-padding: 24px
  gutter: 12px
  component-gap-dense: 4px
  component-gap-normal: 8px
---

## Brand & Style
The design system is engineered for developers who demand high information density and a focused, low-distraction environment. It targets a "2026 dev tool" aesthetic—moving beyond generic SaaS trends into a utilitarian, high-performance interface that feels like an extension of the terminal.

The style is **Minimalist-Technical**. It prioritizes clarity, structural alignment, and speed. The visual language is defined by deep dark backgrounds, subtle micro-borders, and a strict adherence to a "system-first" philosophy where every pixel serves a functional purpose. The emotional response is one of control, reliability, and precision.

## Colors
This design system is dark-mode exclusive to reduce eye strain during long sessions. The core palette uses a sophisticated range of charcoals and blacks to create structural depth without relying on heavy shadows.

- **Foundations:** Use `#09090b` for the main canvas and `#121214` for elevated surface elements like cards or side panels.
- **Borders:** A consistent `#27272a` provides subtle definition between high-density components.
- **Semantic Status:** Color is used sparingly but strictly. Emerald indicates successful synchronization, Amber for version drifts, Gray for inactive states, and Rose for critical failures.
- **Platform Accents:** Use the specific brand colors (Purple, Teal, Blue, Orange) as subtle 2px top-borders or small icons to identify CLI providers at a glance.

## Typography
The typography system uses a dual-font approach to separate UI navigation from technical data. 

- **Geist** handles the primary UI chrome. It is used for navigation, headers, and general descriptive text. Its clean, geometric nature ensures readability at small scales.
- **JetBrains Mono** is the workhorse for all developer-centric data: terminal outputs, file paths, CLI commands, and metadata labels.
- **Hierarchy:** Keep headings compact. For technical labels (e.g., "LAST_SYNCED"), use the `label-caps` style in JetBrains Mono to differentiate metadata from content.

## Layout & Spacing
The layout follows a strict **Fluid Grid** model designed for high-density information display. The base unit is 4px, ensuring all components align to a technical rhythm.

- **Grid:** Use a 12-column grid for main dashboard views. In data-heavy views (like the Matrix Grid), allow columns to shrink to their minimum content width to maximize horizontal real estate.
- **Density:** Favor `component-gap-dense` (4px) for related items like buttons in a group or tags in a list. Use `component-gap-normal` (8px) for separating logical sections.
- **Side Drawers:** Use fixed-width drawers (400px - 560px) that slide from the right for configuration editing, preventing the loss of context in the main dashboard.
- **Sticky Elements:** Table headers and primary action bars must remain sticky to provide constant context in long technical logs.

## Elevation & Depth
Elevation is achieved through **Tonal Layers** and **Low-Contrast Outlines** rather than traditional shadows. 

- **Level 0 (Base):** `#09090b` – The background of the application.
- **Level 1 (Surface):** `#121214` – Used for cards, tables, and sidebars.
- **Level 2 (Overlay):** `#18181b` – Used for modals and the Command Palette (Cmd+K).
- **Borders:** Every interactive element or container should have a 1px border of `#27272a`. For active or focused states, brighten the border to `#3f3f46`. 
- **Shadows:** Use a single, very subtle shadow for overlays: `0 4px 12px rgba(0, 0, 0, 0.5)`. Do not use shadows on base level components.

## Shapes
The shape language is "Soft" but leans toward the sharper end of the spectrum to maintain a precise, engineered feel. 

- **Standard Elements:** Buttons, inputs, and cards use a 4px (0.25rem) radius.
- **Large Containers:** Modals and side drawers use a 6px (0.375rem) radius.
- **Selection Markers:** Use sharp vertical pips (0px radius) on the left side of active list items or navigation links to indicate focus.

## Components
- **Command Palette (Cmd+K):** A centered, high-contrast overlay using JetBrains Mono for search results. Items should include a keyboard shortcut hint on the right.
- **Dense Tables:** 32px row heights. Use `mono-sm` for data cells. On hover, the entire row should highlight with a background of `#18181b`.
- **Buttons:** Small (28px height) and Medium (32px height). Primary buttons are white text on `#27272a` (Ghost style) or solid white for high-priority actions.
- **Status Chips:** Small, rectangular chips with a subtle 10% opacity background of the status color and a solid 1px border. No icons unless space permits.
- **Matrix Grid:** A tight grid of 40x40px cells representing CLI instances or nodes. Use the status colors as small 8px "LED" indicators in the corner of each cell.
- **Input Fields:** Dark backgrounds (`#09090b`), subtle borders, and JetBrains Mono text. Focus state should change the border color to primary white without adding a glow.