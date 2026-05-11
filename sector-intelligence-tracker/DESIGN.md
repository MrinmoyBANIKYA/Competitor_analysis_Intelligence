# Design System Document: Sector Intelligence Tracker

## 1. Overview & Creative North Star: "The Analytical Atelier"
This design system moves away from the rigid, boxy constraints of traditional SaaS dashboards and toward the concept of the **Analytical Atelier**. We treat data not as a series of disconnected widgets, but as a curated editorial experience. 

The "North Star" is **High-Contrast Precision**. We achieve a premium feel by utilizing generous whitespace (the "white background" is our canvas), sophisticated Manrope typography for data storytelling, and a sophisticated layering system that replaces heavy-handed borders with tonal depth. The goal is to make the user feel like they are reading a high-end financial journal rather than a utility tool.

---

## 2. Colors & Surface Philosophy

### The Palette
We utilize a Material-inspired tonal range to ensure the primary blue (`#378ADD`) feels integrated, not just "pasted on."

*   **Primary (`#005ea4`)**: Used for the most critical actions and primary brand touchpoints.
*   **Surface / Background (`#f7f9fb`)**: Our base layer. It’s a "cool" white that reduces eye strain.
*   **Tertiary / Warmth (`#a13a0f`)**: Used sparingly for highlight moments or contrasting data points.

### The "No-Line" Rule
To achieve a signature look, **1px solid borders are strictly prohibited for sectioning.** We define boundaries through:
1.  **Tonal Shifts:** A `surface-container-low` section sitting on a `surface` background.
2.  **Vertical Rhythm:** Using spacing tokens to create distinct visual groups.
3.  **Soft Layering:** If a container needs to stand out, it should use a subtle background color change rather than an outline.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers:
*   **Layer 0 (Background):** `surface` (#f7f9fb)
*   **Layer 1 (Sectioning):** `surface-container-low` (#f2f4f6)
*   **Layer 2 (Cards/Modules):** `surface-container-lowest` (#ffffff)
*   **Layer 3 (Overlays/Popovers):** `surface-bright` (#f7f9fb) with Glassmorphism.

### The "Glass & Gradient" Rule
Floating elements (modals, dropdowns) must utilize **Glassmorphism**. Use a semi-transparent `surface` color with a `backdrop-filter: blur(12px)`. For primary CTAs, use a subtle linear gradient from `primary` (#005ea4) to `primary-container` (#1777c9) at a 135-degree angle to add "soul" to the action.

---

## 3. Typography: Editorial Authority
We pair the geometric stability of **Manrope** for high-level data with the functional clarity of **Inter** for utility.

*   **Display & Headlines (Manrope):** These are your "Editorial" voices. Use `display-md` for high-level KPIs and `headline-sm` for section headers. The wide apertures of Manrope convey modern authority.
*   **Body & Labels (Inter):** The "Workhorse." Use `body-md` for all data tables and descriptions.
*   **The Power of Scale:** Don't be afraid of the contrast between a `display-lg` KPI value and a `label-sm` unit descriptor. This creates a clear hierarchy of importance.

---

## 4. Elevation & Depth: Tonal Layering

### The Layering Principle
Depth is achieved by "stacking" surface tiers.
*   **Example:** Place a White card (`surface-container-lowest`) on a light grey background (`surface-container-low`). This creates a soft, natural lift that feels architectural.

### Ambient Shadows
Shadows must be "ghostly" and organic.
*   **Spec:** `0px 12px 32px rgba(25, 28, 30, 0.04)`.
*   The shadow should never be pure black; it should be a low-opacity tint of the `on-surface` color to mimic natural ambient light.

### The "Ghost Border" Fallback
If accessibility requires a border (e.g., in high-density tables), use the **Ghost Border**: `outline-variant` (#c0c7d3) at **20% opacity**. This provides a guide without cluttering the visual field.

---

## 5. Components

### Cards & Data Modules
*   **Execution:** No dividers. Separate content using `32px` (or `2rem`) of vertical whitespace.
*   **Radius:** Use `xl` (0.75rem) for main dashboard cards to soften the data-heavy environment.

### Buttons
*   **Primary:** Gradient fill (`primary` to `primary-container`), `md` (0.375rem) radius, white text.
*   **Secondary:** `surface-container-high` background with `on-surface` text. No border.
*   **Tertiary:** Ghost style. No background/border until hover.

### Inputs & Search
*   **Style:** `surface-container-lowest` background with a `Ghost Border`.
*   **Focus State:** Shift the border to 100% opacity `primary` and add a subtle `primary-fixed` (low opacity) outer glow.

### Data Visualization (6-Color Palette)
Charts must use the following sequence for maximum distinction:
1.  **Blue:** `primary` (#005ea4)
2.  **Teal:** `#008080` (Custom)
3.  **Coral:** `tertiary` (#a13a0f)
4.  **Purple:** `#6A5ACD` (Custom)
5.  **Amber:** `#FFBF00` (Custom)
6.  **Pink:** `#DB7093` (Custom)
*   *Note:* Ensure all chart paths have a `2px` stroke width for clarity.

### Contextual Tooltips
*   **Style:** `inverse-surface` background with `inverse-on-surface` text.
*   **Motion:** 150ms ease-out fade with a 4px vertical slide.

---

## 6. Do’s and Don'ts

### Do:
*   **Do** use asymmetrical layouts. A 2/3 width chart next to a 1/3 width insights panel feels more "designed" than two equal halves.
*   **Do** use `letter-spacing: -0.02em` on Manrope headlines to give them a premium, tight editorial feel.
*   **Do** leverage `surface-container-highest` for subtle hover states on list items rather than a border.

### Don't:
*   **Don't** use 100% black text. Always use `on-surface` (#191c1e) for better readability and a more "expensive" ink-on-paper look.
*   **Don't** use standard 1px grey dividers to separate list items. Use whitespace or a `5%` opacity `outline-variant` line that fades out at the edges.
*   **Don't** use "Default" blue (#0000FF). Only use the specific `primary` tokens provided.

---

## 7. Spacing & Grid
This system thrives on **Vertical Breathability**.
*   **Base Unit:** 4px
*   **Dashboard Padding:** Use `48px` (3rem) for page margins to prevent the "cramped" SaaS feel.
*   **Component Spacing:** Use `24px` (1.5rem) between cards to allow the background tonal shifts to act as natural gutters.