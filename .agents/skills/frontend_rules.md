## 2024-05-24 - Inline remove action on dynamic rows
**Learning:** Adding a way to dynamically add elements to a form without a way to easily remove them leads to poor UX. Using standard icons like a trash can and visually associating them with the added item is a standard way to implement removal.
**Action:** When creating forms with dynamic multi-input elements, always include a way to easily remove the elements with an accessible button.
## 2024-05-24 - Inline remove action on dynamic rows
**Learning:** Adding a way to dynamically add elements to a form without a way to easily remove them leads to poor UX. Using standard icons like a trash can and visually associating them with the added item is a standard way to implement removal.
**Action:** When creating forms with dynamic multi-input elements, always include a way to easily remove the elements with an accessible button.
## 2024-05-18 - Missing Active State Indication in Navbars
**Learning:** Found that the main navigation in `base.html` used simple anchor tags without any `active` class or `aria-current="page"` attributes to indicate the currently viewed page. This can be confusing for screen reader users and users with cognitive disabilities.
**Action:** Always wrap navbar links in `nav-item` elements and use Jinja's `request.endpoint` to dynamically append `active` classes and `aria-current="page"` for accessibility.

## 2024-05-13 - Fix Silent UX Failures with Missing Bootstrap JS/Icons
**Learning:** When using Bootstrap 5, interactive components (like Modals) and custom icons (like bi-clipboard) fail silently if the corresponding Bootstrap JS bundle and Bootstrap Icons CSS are missing from the base template. This leads to confusing empty buttons and broken modals with no immediate console errors in some environments.
**Action:** Always verify that both the CSS and JS bundles for Bootstrap (and its icon set) are properly linked in the base layout when utilizing its advanced interactive UI components.

## 2024-05-17 - [Handle Synchronous Form Loading States Safely]
**Learning:** Adding disabled=true directly inside a form submit event or click handler can immediately block the native form submission from firing in some browsers, leaving the user stuck with a spinning button but no request sent.
**Action:** When adding loading states to synchronous forms (like data fetching), always wrap the disabled state change inside a setTimeout. This allows the event loop to finish executing the native form submission trigger before the button is actually disabled in the DOM.

## 2025-03-01 - Sync Action Loading States
**Learning:** Synchronous actions (like grid search) that take a long time to return a response leave the user with no feedback and a frozen UI, often leading to duplicate clicks and confusion.
**Action:** Always add loading spinners and disable submit buttons for synchronous form submissions using the setTimeout pattern to prevent duplicate submissions and provide immediate visual feedback.

## 2025-03-01 - Proper Grouping of Multi-Input Fields
**Learning:** Using a single `<label>` element for a row of multiple standalone `<input>` elements (e.g. three separate date pickers for a "Start dates" field) causes screen readers to lose context, as they read the inputs without associating them with the label.
**Action:** Always group related multi-input fields using a `<fieldset>` and a `<legend>` to provide the overarching context, while still giving each individual `<input>` a specific `aria-label` or `id`+`for` to uniquely identify its purpose.

## 2025-03-01 - Explicit Form Labels
**Learning:** Using implicit `<label>` wrapping around form inputs (like `<label>Name <input></label>`) can lead to styling issues with Bootstrap 5 and reduced click areas, and is sometimes poorly supported by older assistive technologies compared to explicit labeling.
**Action:** Always explicitly associate `<label>` elements with their corresponding inputs using matching `for` and `id` attributes, rather than relying on implicit wrapping.
## 2025-03-01 - Explicit Label Association
**Learning:** Implicit label wrapping (e.g. `<label>Name <input></label>`) or using labels completely disconnected from their inputs (e.g., `<label>Name</label><input>`) can cause screen readers to fail to announce the label when the input receives focus. It also prevents native browser behaviors like focusing the input when the label text is clicked, and may break specific framework styles (like Bootstrap's form-label spacing).
**Action:** For form accessibility and proper styling, always explicitly associate `<label>` elements with their corresponding inputs using matching `for` and `id` attributes, rather than relying on implicit wrapping or visual proximity.
## 2025-03-01 - Native HTML5 Validation for Configuration Variables
**Learning:** Permitting invalid inputs (such as negative numbers for periods/lookbacks or unbounded numbers for percentages/RSI) in financial configuration forms causes backtest jobs to fail immediately upon execution, creating a frustrating loop for the user.
**Action:** When creating forms for numerical configuration parameters (like lookbacks, thresholds, etc.), always use native HTML5 validation attributes (`min`, `max`, `step`) to provide immediate, inline validation feedback in the browser and prevent invalid state submissions.
## 2025-03-01 - Native Multiple Select Accessibility
**Learning:** Native `<select multiple>` elements do not provide intrinsic instructions or visual clues on how to select more than one option (which typically requires holding Ctrl or Cmd), leading to user frustration. Screen readers also do not inherently announce this requirement.
**Action:** Always provide explicit, visually visible helper text below native multiple selects explaining the keyboard modifiers needed, and associate it with the input using `aria-describedby` for accessibility.
## 2025-03-01 - Empty States Enhance Onboarding
**Learning:** Tables displaying complex data (like backtest results or portfolio trades) that simply show "No data yet" appear broken or intimidating to new users. Replacing these with styled empty states including semantic icons and clear calls-to-action (like a "Run a Backtest" button) immediately directs user flow and reduces initial friction.
**Action:** When creating new data tables or lists, always include a designed empty state (using Bootstrap utility classes like `text-center text-muted py-5 bg-white border`) with a relevant icon and actionable link instead of plain text.

## 2024-03-24 - Do not rely purely on color to convey state
**Learning:** Using only text color (e.g. green text) to indicate that an item is 'downloaded' or selected is a WCAG accessibility violation because screen readers and colorblind users cannot easily perceive the state change.
**Action:** Always pair color changes with an explicit text indicator or icon (like a checkmark ✓) so state is perceivable in multiple ways.

## 2025-03-01 - Dynamic Linking of Paired Date Bounds
**Learning:** When users must select a "start" and "end" date range, native HTML5 `<input type="date">` allows selecting an end date before a start date. This leads to frustrating form validation errors on submission and poor usability.
**Action:** Always link paired date pickers using JavaScript by setting the `min` attribute of the end date when the start date changes, and setting the `max` attribute of the start date when the end date changes, ensuring the browser naturally restricts invalid range combinations inline.
## 2025-03-05 - Enhance Date Picker Range Linking and Visual Indicators
**Learning:** Adding dynamic linking between 'start' and 'end' date pickers directly in the DOM (setting `min` and `max` dynamically via JS) is a low-effort, high-impact UX win that prevents invalid date range submissions and user frustration before they hit the server. Combining this with visually explicit required indicators ensures clarity for accessibility and usability.
**Action:** When working with forms involving dependent date ranges, immediately consider adding frontend dynamic boundary constraints to the input attributes and visual asterisks for required fields.
## 2026-04-14 - Native Confirmations for Destructive Actions
**Learning:** Destructive actions like stopping a live trading engine (which halts all active evaluations and automated trading) should never execute immediately on a single click, as this can lead to accidental disruption of critical systems and poor user experience.
**Action:** When adding buttons that perform destructive or highly disruptive actions, always include a native browser confirmation dialog (e.g., `onsubmit="return confirm(...)"`) to verify the user's intent before submission.

## 2026-04-26 - Implement Skip to Main Content Links Properly
**Learning:** Keyboard-only and screen-reader users suffer when they have to tab through repetitive navigation blocks on every page. Adding a "Skip to main content" link at the start of the body is a crucial accessibility win. However, it requires making the target container focusable programmatically (using `tabindex="-1"`) and styling it appropriately to avoid a jarring focus ring (using `style="outline: none;"`).
**Action:** Always include a "Skip to main content" link (with classes like `visually-hidden-focusable`) at the very top of base HTML layouts and ensure the target ID container has `tabindex="-1"` and `outline: none`.

## 2025-05-24 - Validate Numeric Config Parameters with HTML5

**Learning:** Permitting invalid inputs (such as negative numbers for periods/lookbacks or unbounded numbers for percentages/RSI) in financial configuration forms causes backtest jobs to fail immediately upon execution, creating a frustrating loop for the user. While validation on the backend is necessary, immediate frontend validation avoids a slow round-trip.

**Action:** When creating forms for numerical configuration parameters (like lookbacks, thresholds, etc.), always use native HTML5 validation attributes (`min`, `max`, `step`) to provide immediate, inline validation feedback in the browser and prevent invalid state submissions.
## 2025-05-24 - Table Responsiveness on Mobile Layouts
**Learning:** Standard Bootstrap tables lacking the `.table-responsive` wrapper class will force horizontal overflow on narrow mobile screens, breaking the primary page layout and making navigation extremely difficult.
**Action:** Always wrap data-heavy HTML `<table>` elements with `<div class="table-responsive">` to ensure horizontal scrolling is scoped to the table itself, rather than breaking the full page width on small devices.
## 2024-05-07 - Handling wide tables on mobile screens
**Learning:** Large data tables that overflow horizontally on mobile screens break the page layout and create a frustrating, horizontally-scrolling experience that is difficult to navigate.
**Action:** Always wrap large data tables in a `<div class="table-responsive">` to allow the table itself to scroll horizontally without breaking the parent container's layout.

## 2024-05-07 - JS SyntaxErrors in HTML templates
**Learning:** Duplicate variable declarations (e.g. `const startInput = ...`) in inline `<script>` tags within HTML templates cause `SyntaxError` and silently break the rest of the JavaScript execution on the page, leaving interactive elements dead.
**Action:** Always verify inline scripts for duplicate declarations, especially when combining or copying snippets.

## 2026-05-10 - Semantic Buttons for Interactive Elements
**Learning:** Using `<span>` or `<div>` elements with `onclick` handlers for interactive UI components (like opening error modals) removes them from the native tab order, making them completely inaccessible to keyboard and screen-reader users without complex custom role/tabindex management.
**Action:** Always use semantic `<button>` elements for inline interactive actions. Use Bootstrap utility classes like `btn btn-link text-decoration-none shadow-none p-0 align-baseline` to strip default styling while preserving native focus and interaction capabilities.

## 2025-06-25 - Pattern Validation for Custom Inputs
**Learning:** Custom input formats, like comma-separated lists for grid search parameters, can lead to backend crashes and generic "500 Internal Server Error" pages if a user makes a typo. Waiting for backend validation causes a slow round-trip for basic data-entry errors.
**Action:** When a text input expects a specific custom format (like comma-separated numbers), always apply an HTML5 `pattern` attribute with an appropriate regex (e.g. `^\s*\d+\s*(,\s*\d+\s*)*$`). This provides immediate inline validation before the form is submitted.

## 2025-06-25 - Concise Labels with aria-describedby
**Learning:** Cluttering `<label>` elements with verbose formatting examples (e.g., "RSI Periods (e.g. 10, 14)") forces screen readers to read the entire string before the user even understands what the input is for. It also creates visual noise on the page.
**Action:** Keep `<label>` elements concise and clear. Move formatting examples or lengthy helper text into a separate element (like `<div class="form-text">`) below the input, and associate it with the input using the `aria-describedby` attribute to maintain semantic connection without upfront clutter.
