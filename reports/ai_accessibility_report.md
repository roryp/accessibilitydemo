# AI-Powered Accessibility Analysis Report

*Analysis performed via the GitHub Copilot SDK (model: default)*

This report provides accessibility analysis based on WCAG 2.1 AA guidelines.

## Analysis: accessibility-issues-demo.html

# Accessibility Audit Report
**Document:** "Accessibility Issues Demo – What NOT to Do"
**Standard applied:** WCAG 2.1 Level AA (with Section 508 / EN 301 549 equivalence notes)
**Audit date:** 9 October 2026
**Method:** Static code review + computed contrast analysis + simulated AT behaviour (NVDA/JAWS/VoiceOver patterns)

---

## 1. Executive Summary

The page fails WCAG 2.1 AA on **at least 14 distinct Success Criteria**. Several failures are *blocking* — a screen reader user cannot determine the purpose of the chart image, cannot reliably complete the contact form, and cannot perceive most text due to contrast ratios as low as **1.14:1** (minimum required: 4.5:1).

Credit where due: the page *does* include a skip link with a visible-on-focus style, keyboard handlers on custom widgets, `role`/`aria-expanded` management on the dropdown, and roving focus in the menu. These are better than typical "bad demo" code, but each still has defects that prevent conformance.

### Conformance Scorecard

| WCAG SC | Level | Status | Severity |
|---|---|---|---|
| 1.1.1 Non-text Content | A | ❌ Fail | Critical |
| 1.2.1 Audio-only/Video-only (Prerecorded) | A | ❌ Fail | High |
| 1.2.2 Captions (Prerecorded) | A | ❌ Fail | High |
| 1.2.3 / 1.2.5 Audio Description | A/AA | ❌ Fail | High |
| 1.3.1 Info and Relationships | A | ❌ Fail | Critical |
| 1.3.5 Identify Input Purpose | AA | ❌ Fail | Medium |
| 1.4.2 Audio Control | A | ⚠️ At risk | High |
| 1.4.3 Contrast (Minimum) | AA | ❌ Fail | Critical |
| 1.4.4 Resize Text | AA | ⚠️ At risk | Medium |
| 1.4.10 Reflow | AA | ⚠️ At risk | Medium |
| 1.4.11 Non-text Contrast | AA | ⚠️ At risk | Medium |
| 2.1.1 Keyboard | A | ⚠️ Partial | Medium |
| 2.2.2 Pause, Stop, Hide | A | ❌ Fail | Critical |
| 2.4.1 Bypass Blocks | A | ⚠️ Partial | Medium |
| 2.4.4 Link Purpose (In Context) | A | ❌ Fail | High |
| 2.4.6 Headings and Labels | AA | ❌ Fail | High |
| 2.4.7 Focus Visible | AA | ⚠️ At risk | Medium |
| 3.1.1 Language of Page | A | ❌ Fail | Critical |
| 3.3.1 Error Identification | A | ❌ Fail | High |
| 3.3.2 Labels or Instructions | A | ❌ Fail | Critical |
| 3.3.3 Error Suggestion | AA | ❌ Fail | Medium |
| 4.1.2 Name, Role, Value | A | ❌ Fail | Critical |
| 4.1.3 Status Messages | AA | ❌ Fail | Medium |

---

## 2. Document Structure & Semantics

### FINDING 2.1 — Missing `lang` attribute
- **Severity:** Critical
- **WCAG:** 3.1.1 Language of Page (A)
- **Location:** `<html>` (line 2)
- **Issue:** No language declared. Screen readers fall back to the user's OS voice/language profile; English content read by a Spanish synthesizer is unintelligible. Also breaks automatic translation and hyphenation.

```html
<!-- BEFORE -->
<html>

<!-- AFTER -->
<html lang="en">
```
- **User impact:** Blind and low-vision screen reader users, users of translation tools, braille display users (braille contraction tables are language-specific).

---

### FINDING 2.2 — Missing charset and viewport meta
- **Severity:** High
- **WCAG:** 1.4.4 Resize Text (AA), 1.4.10 Reflow (AA) — plus HTML validity
- **Location:** `<head>`
- **Issue:** No `<meta charset>` (the emoji `🚨` and `▼` may mojibake). No `<meta name="viewport">`, so mobile browsers apply a 980px virtual viewport and shrink everything, defeating 320px reflow and text resize on mobile.

```html
<!-- BEFORE -->
<head>
    <title>…</title>

<!-- AFTER -->
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>…</title>
```
- **User impact:** Low-vision mobile users who zoom; users with cognitive disabilities who need larger text.

---

### FINDING 2.3 — No landmark regions
- **Severity:** High
- **WCAG:** 1.3.1 Info and Relationships (A); 2.4.1 Bypass Blocks (A) support
- **Location:** `<body>` → `<div class="container" id="main-content">`
- **Issue:** The entire page is `<div>` soup. There is no `<main>`, `<header>`, `<nav>`, or `<footer>`. Screen reader users navigate by landmark (NVDA `D` key, VoiceOver rotor); here the rotor landmark list is empty, forcing linear reading of the whole document.

```html
<!-- BEFORE -->
<div class="container" id="main-content">

<!-- AFTER -->
<main class="container" id="main-content" tabindex="-1">
```
- **User impact:** Screen reader users lose the primary structural navigation mechanism.

---

### FINDING 2.4 — Skip link target is not focusable
- **Severity:** Medium
- **WCAG:** 2.4.1 Bypass Blocks (A), 2.4.3 Focus Order (A)
- **Location:** `<a href="#main-content">` → `<div id="main-content">`
- **Issue:** The skip link is well implemented visually (off-screen, revealed on `:focus`), but the target is a non-focusable `<div>`. In several browser/AT combinations (historically IE/Edge, and some Safari+VoiceOver states) the viewport scrolls but **keyboard focus stays on the skip link**, so the next Tab returns the user to the top of the page. Add `tabindex="-1"` to the target (see fix in 2.3).
- **Additional note:** With only one skip target and no navigation block, the skip link currently bypasses nothing. Keep it, but ensure real landmarks exist.
- **User impact:** Keyboard-only and screen reader users; the bypass mechanism silently fails.

---

### FINDING 2.5 — Broken heading hierarchy
- **Severity:** High
- **WCAG:** 1.3.1 (A), 2.4.6 Headings and Labels (AA)
- **Location:**
```html
<h3>Welcome to Our Website</h3>
<h1>This heading order is wrong</h1>
```
- **Issue:** The document starts at `<h3>`, then jumps backwards to `<h1>`. Heading levels must describe a nested outline; skipping levels and reversing order makes the programmatic structure meaningless. The `<h1>` text ("This heading order is wrong") is also not a descriptive page title. Additionally, the `<h2>Contact Form</h2>` and the table and dropdown sections have inconsistent/absent headings.

```html
<!-- BEFORE -->
<div>
    <h3>Welcome to Our Website</h3>
    <h1>This heading order is wrong</h1>
</div>

<!-- AFTER -->
<h1>Welcome to Our Website</h1>
<h2>About our products</h2>
<!-- …then h2 for Contact Form, h2 for Product availability, h2 for Country selection -->
```
- **User impact:** 67% of screen reader users navigate primarily by heading (WebAIM Survey #10). A broken outline makes the page unnavigable and misrepresents content importance.

---

### FINDING 2.6 — Page title
- **Severity:** Low (informational)
- **WCAG:** 2.4.2 Page Titled (A) — **passes**
- **Note:** The title is unique and descriptive. For a production site, use the pattern `Page topic – Site name` and ensure it updates on SPA route changes.

---

## 3. Colour & Contrast

All ratios below computed per WCAG relative-luminance formula.

### FINDING 3.1 — Body text contrast 2.20:1
- **Severity:** Critical
- **WCAG:** 1.4.3 Contrast (Minimum) (AA) — requires 4.5:1 normal text / 3:1 large text
- **Location:** `body { background-color:#00bbff; color:#ffffff; }`
- **Measured:** `#ffffff` on `#00bbff` = **2.20:1** — fails even the 3:1 large-text threshold.

```css
/* BEFORE */
body { background-color: #00bbff; color: #ffffff; }

/* AFTER — 12.6:1 */
body { background-color: #ffffff; color: #1a1a1a; }
/* If the brand cyan must be kept as a background: */
.brand-band { background-color: #00bbff; color: #000000; } /* 9.5:1 */
```
- **User impact:** Users with low vision, cataracts, age-related contrast loss, colour-vision deficiency, and anyone on a glare-affected screen cannot read the page.

### FINDING 3.2 — `.low-contrast` block at 1.14:1
- **Severity:** Critical
- **WCAG:** 1.4.3 (AA)
- **Location:** `.low-contrast { background:#f0f0f0; color:#ffffff; }`
- **Measured:** **1.14:1**. This is effectively invisible text (white on near-white).

```css
/* AFTER — 13.6:1 */
.callout { background-color: #f0f0f0; color: #1a1a1a; padding: 10px; }
```
- **User impact:** Content is unreadable for *all* sighted users, not just those with disabilities. Screen readers still announce it, creating a jarring mismatch.

### FINDING 3.3 — Red submit control at 4.00:1
- **Severity:** High
- **WCAG:** 1.4.3 (AA)
- **Location:** `.button-like { background-color: red; color: white; }`
- **Measured:** `#ffffff` on `#ff0000` = **4.00:1** — fails the 4.5:1 requirement for normal-size text.

```css
/* AFTER — 5.9:1 */
.btn-primary { background-color: #c00000; color: #ffffff; }
```
- **Note:** Pure red on white is also the worst-case colour for protanopia. Prefer a darker red or a blue/neutral primary.

### FINDING 3.4 — Non-text contrast of UI boundaries not guaranteed
- **Severity:** Medium
- **WCAG:** 1.4.11 Non-text Contrast (AA)
- **Location:** Custom dropdown `style="border:1px solid black"`; default-styled `<input>`/`<textarea>` elements rendered on `#00bbff`.
- **Issue:** Default browser input borders (~`#767676`) against the cyan background measure below 3:1 in several combinations, so the boundary of the control may not be perceivable. Component borders and focus indicators must reach 3:1 against adjacent colours.

```css
/* AFTER */
input, textarea, select { border: 2px solid #595959; background:#fff; color:#1a1a1a; }
```

### FINDING 3.5 — Tiny fixed-size text (8px)
- **Severity:** Medium
- **WCAG:** 1.4.4 Resize Text (AA), 1.4.12 Text Spacing (AA) — best practice
- **Location:** `.small-text { font-size: 8px; }`
- **Clarification:** WCAG does **not** mandate a minimum font size (the inline comment in the source is inaccurate). The real failure risk is that 8px text combined with the missing viewport meta cannot be enlarged to 200% on mobile without loss of content, and it is a documented barrier for low-vision and dyslexic users.

```css
/* BEFORE */
.small-text { font-size: 8px; }

/* AFTER */
.fine-print { font-size: 0.875rem; /* 14px, scales with user preference */ }
```

### FINDING 3.6 — Colour/styling as the only indicator of urgency
- **Severity:** Medium
- **WCAG:** 1.4.1 Use of Color (A), 1.3.3 Sensory Characteristics (A)
- **Location:** `<p class="blinking">🚨 URGENT: …</p>`
- **Issue:** Urgency is conveyed by blinking and emoji. Emoji accessible names are verbose and inconsistent ("police car light" repeated twice). Use text plus a semantic role.

---

## 4. Images & Media

### FINDING 4.1 — Informative image with no `alt`
- **Severity:** Critical
- **WCAG:** 1.1.1 Non-text Content (A)
- **Location:** `<img src="important-chart.jpg" width="300" height="200">`
- **Issue:** No `alt` attribute at all. Screen readers announce the filename ("important chart dot jpg, graphic"), which is not an equivalent. Charts are *complex images* requiring both a short name and a long description (WCAG Technique G92/H45).

```html
<!-- BEFORE -->
<img src="important-chart.jpg" width="300" height="200">

<!-- AFTER -->
<figure>
  <img src="important-chart.jpg" width="300" height="200"
       alt="Bar chart: quarterly sales 2026. Q1 $1.2M, Q2 $1.5M, Q3 $1.1M, Q4 $1.9M.">
  <figcaption>
    Quarterly sales, 2026.
    <a href="#chart-data">View the data as a table</a>.
  </figcaption>
</figure>
<!-- Plus a real <table id="chart-data"> with the underlying values -->
```
- **User impact:** Blind users lose the entire data content; users with cognitive disabilities benefit from the tabular alternative.

### FINDING 4.2 — Decorative image with verbose `alt`
- **Severity:** Medium
- **WCAG:** 1.1.1 (A) — failure F39 (non-null alt on decorative image)
- **Location:** `<img src="decorative-icon.png" alt="A beautiful decorative image that adds no informational value but has unnecessary alt text">`
- **Issue:** The alt text itself states the image carries no information, yet forces 16 words of noise into the reading order.

```html
<!-- AFTER -->
<img src="decorative-icon.png" alt="" role="presentation">
<!-- or move it to CSS background-image entirely -->
```

### FINDING 4.3 — Autoplaying, looping video with no controls, captions, or description
- **Severity:** High (Critical if the file contains audio)
- **WCAG:** 1.2.1 (A), 1.2.2 Captions (A), 1.2.3/1.2.5 Audio Description (A/AA), 1.4.2 Audio Control (A), 2.2.2 Pause Stop Hide (A)
- **Location:**
```html
<video width="320" height="240" autoplay loop>
    <source src="background-video.mp4" type="video/mp4">
</video>
```
- **Issues:**
  1. `autoplay` + `loop` + **no `controls`** = moving content lasting >5 s with **no mechanism to pause, stop, or hide** → direct 2.2.2 failure.
  2. If the file has an audio track that plays >3 s automatically, 1.4.2 fails (no volume/stop control).
  3. No `<track kind="captions">` → 1.2.2 fails for deaf/HoH users.
  4. No audio description or transcript → 1.2.3/1.2.5 fail.
  5. No fallback content between `<video>` tags.
  6. No `prefers-reduced-motion` handling — vestibular-disorder trigger.

```html
<!-- AFTER -->
<video width="320" height="240" controls preload="metadata"
       muted playsinline poster="video-poster.jpg">
  <source src="background-video.mp4" type="video/mp4">
  <track kind="captions" src="captions-en.vtt" srclang="en" label="English" default>
  <track kind="descriptions" src="descriptions-en.vtt" srclang="en" label="English descriptions">
  <p>Your browser cannot play this video.
     <a href="background-video.mp4">Download the video (MP4)</a> or
     <a href="transcript.html">read the transcript</a>.</p>
</video>
```
```css
@media (prefers-reduced-motion: reduce) {
  video[autoplay] { /* ship without autoplay, or */ animation: none; }
}
```
- **User impact:** Deaf users get no content; screen reader users hear competing audio; users with ADHD/cognitive disabilities are distracted and cannot stop the motion; vestibular users may experience nausea.

### FINDING 4.4 — Infinitely blinking content
- **Severity:** Critical
- **WCAG:** 2.2.2 Pause, Stop, Hide (A); 2.3.1 Three Flashes (A) — see note
- **Location:** `.blinking { animation: blink 1s linear infinite; }`
- **Issue:** Content blinks indefinitely with no pause mechanism → **2.2.2 failure**. Note for accuracy: at 1 Hz this is *below* the 3-flashes-per-second general flash threshold, so **2.3.1 is not technically violated** (the source comment's "can cause seizures" claim overstates it), but the 2.2.2 failure is absolute, and the pattern is a well-documented trigger for migraine, ADHD distraction, and reading difficulty.

```html
<!-- BEFORE -->
<p class="blinking">🚨 URGENT: This text blinks and can cause seizures! 🚨</p>

<!-- AFTER -->
<div role="alert" class="alert alert--urgent">
  <strong>Urgent:</strong> Service maintenance begins at 10:00 PM tonight.
</div>
```
```css
.alert--urgent{background:#8a1c1c;color:#fff;border-left:6px solid #ffd400;padding:12px}
@media (prefers-reduced-motion: no-preference){
  /* if any emphasis animation is used, run it a finite number of times (<5s) */
}
```

---

## 5. Forms & Interactive Elements

### FINDING 5.1 — Inputs with no programmatic label (3 of 4 fields)
- **Severity:** Critical
- **WCAG:** 1.3.1 (A), 3.3.2 Labels or Instructions (A), 4.1.2 Name, Role, Value (A), 2.4.6 (AA)
- **Location:**
```html
<p>Name:</p>   <input type="text" placeholder="Enter your name">
<p>Email:</p>  <input type="email">
<p>Message:</p><textarea placeholder="Your message here"></textarea>
```
- **Issues:**
  - `<p>` text is visually adjacent but has **no programmatic association**. Screen readers announce "edit, blank" / "edit text, blank".
  - `placeholder` is **not** an accessible label substitute (WCAG failure F82 territory): it disappears on input, has low contrast by default, is unreliable in older AT, and is lost for speech-input users who say "click Name".
  - The email field has **neither** label nor placeholder — completely unidentified.
  - Clicking the `<p>` does not focus the field (lost hit area).

```html
<!-- AFTER -->
<div class="field">
  <label for="name">Full name <span aria-hidden="true">*</span></label>
  <input type="text" id="name" name="name" autocomplete="name"
         required aria-required="true" aria-describedby="name-hint name-err">
  <p id="name-hint" class="hint">First and last name.</p>
  <p id="name-err" class="error" hidden></p>
</div>

<div class="field">
  <label for="email">Email address</label>
  <input type="email" id="email" name="email" autocomplete="email"
         required aria-required="true" aria-describedby="email-err">
  <p id="email-err" class="error" hidden></p>
</div>

<div class="field">
  <label for="message">Message</label>
  <textarea id="message" name="message" rows="5"></textarea>
</div>
```
- **User impact:** Screen reader users cannot determine what to type; speech-recognition users cannot target fields by name; users with memory/attention disabilities lose the placeholder hint once typing starts.

### FINDING 5.2 — Label hidden with `display:none`
- **Severity:** High
- **WCAG:** 1.3.1 (A), 3.3.2 (A)
- **Location:** `<label class="hidden-label" for="phone">Phone:</label>` with `.hidden-label{display:none}`
- **Issue:** `display:none` removes the element from the accessibility tree. Although most modern browsers *do* still compute the accessible name from a `for`-associated hidden `<label>`, this behaviour is inconsistent across engines and is explicitly discouraged; more importantly, **sighted** users lose the visible label entirely, leaving only a placeholder (3.3.2 failure). If a label must be visually hidden, use the clip pattern — never `display:none`.

```css
/* BEFORE */
.hidden-label { display: none; }

/* AFTER — visually hidden but exposed to AT */
.visually-hidden{
  position:absolute; width:1px; height:1px; margin:-1px;
  padding:0; overflow:hidden; clip:rect(0 0 0 0); clip-path:inset(50%); white-space:nowrap; border:0;
}
```
```html
<label for="phone">Phone number <span class="hint">(optional)</span></label>
<input type="tel" id="phone" name="phone" autocomplete="tel">
```

### FINDING 5.3 — No `autocomplete` attributes
- **Severity:** Medium
- **WCAG:** 1.3.5 Identify Input Purpose (AA)
- **Location:** All inputs collecting user data (name, email, phone).
- **Issue:** AA requires that inputs collecting information *about the user* expose their purpose programmatically via the HTML autocomplete token list.
- **Fix:** `autocomplete="name"`, `autocomplete="email"`, `autocomplete="tel"` (shown above).
- **User impact:** Users with motor impairments and cognitive disabilities lose auto-fill and personalised-icon assistive tooling.

### FINDING 5.4 — Submit control is a `<div role="button">`, not a `<button>`
- **Severity:** High
- **WCAG:** 4.1.2 (A), 2.1.1 Keyboard (A), 3.2.2 On Input (A)
- **Location:**
```html
<div class="button-like" onclick="submitForm()" onkeydown="handleButtonKeydown(event, submitForm)" tabindex="0" role="button">Submit</div>
```
- **Issues (this is better than the usual bare `div`, but still non-conforming):**
  1. It is **not a form submit control**, so pressing **Enter** inside the Name/Email fields does not submit the form — a standard, expected keyboard behaviour is lost (implicit submission).
  2. Space activation is bound to `keydown`; native buttons activate on `keyup` for Space. Holding Space on a `div` will auto-repeat the callback, firing `submitForm()` dozens of times.
  3. `event.key === ' '` works, but legacy AT/browsers report `'Spacebar'`; no fallback.
  4. No `disabled` state, no `type`, no form association, not reachable by speech command "click Submit button" in some engines.
  5. No custom `:focus-visible` style, and the browser default focus ring may fall below 3:1 against the red background.

```html
<!-- AFTER -->
<button type="submit" class="btn-primary">Send message</button>
```
```css
.btn-primary:focus-visible{ outline:3px solid #0b57d0; outline-offset:2px; }
```
> Deleting the keyboard shim entirely is the fix. Every line of `handleButtonKeydown` exists to re-implement `<button>` imperfectly.

### FINDING 5.5 — No error identification, suggestion, or validation feedback
- **Severity:** High
- **WCAG:** 3.3.1 Error Identification (A), 3.3.3 Error Suggestion (AA), 4.1.3 Status Messages (AA)
- **Location:** `submitForm()` → `alert("Form submitted!")`
- **Issues:**
  - No required-field indication, no client-side validation, no error container.
  - `alert()` is a modal interruption; while screen readers do read it, it is not a WCAG-compliant status-message pattern, cannot be re-read, and destroys context on mobile.
  - No programmatic association between an error and its field (`aria-describedby` / `aria-invalid`).

```html
<!-- AFTER: error summary + inline errors + live region -->
<div id="form-status" role="status" aria-live="polite" class="visually-hidden"></div>

<div id="error-summary" role="alert" tabindex="-1" hidden>
  <h3>There is a problem</h3>
  <ul id="error-list"></ul>
</div>
```
```js
function showError(input, msg){
  const err = document.getElementById(input.id + '-err');
  err.textContent = msg; err.hidden = false;
  input.setAttribute('aria-invalid','true');
  input.setAttribute('aria-describedby', (input.id+'-hint '+input.id+'-err').trim());
}
form.addEventListener('submit', e => {
  // validate…; if invalid: e.preventDefault(); build summary; summary.hidden=false; summary.focus();
  // if valid: document.getElementById('form-status').textContent = 'Your message was sent.';
});
```
- **User impact:** Blind users and users with cognitive disabilities cannot recover from mistakes; errors announced only visually (or via a dismissed alert) are lost.

### FINDING 5.6 — No grouping / no `<fieldset>` where needed
- **Severity:** Low
- **WCAG:** 1.3.1 (A)
- **Note:** No radio/checkbox groups exist today, so `<fieldset>` is not strictly required. However, the form has no accessible name. Add `<form aria-labelledby="contact-heading">` referencing the `<h2>`, so the form landmark is announced meaningfully.

---

## 6. Links

### FINDING 6.1 — Non-descriptive link text
- **Severity:** High
- **WCAG:** 2.4.4 Link Purpose (In Context) (A); 2.4.9 (AAA) advisory
- **Location:** `<a href="info.html">click here</a>` / `<a href="details.html">read more</a>`
- **Issue:** Screen reader users list links out of context (NVDA Insert+F7). The list reads "click here, read more" — purposeless. "Click here" also assumes a pointing device (3.3.2/1.3.3 concern for touch and switch users).

```html
<!-- BEFORE -->
<p>For more information, <a href="info.html">click here</a> or <a href="details.html">read more</a></p>

<!-- AFTER -->
<p>Read our <a href="info.html">product information guide</a>
   or see <a href="details.html">detailed technical specifications</a>.</p>

<!-- If link text must stay short: -->
<a href="details.html">Read more<span class="visually-hidden"> about Widget A specifications</span></a>
```

---

## 7. Data Tables

### FINDING 7.1 — Table has no header cells, caption, or scope
- **Severity:** High
- **WCAG:** 1.3.1 Info and Relationships (A)
- **Location:** The product table — the header row uses `<td>`, not `<th>`.
- **Issue:** Without `<th>` + `scope`, AT cannot announce "Price, $29.99" when navigating cells. A blind user reading cell-by-cell hears only "$29.99" with no idea which column it belongs to. There is also no `<caption>`, `<thead>`, or `<tbody>`.

```html
<!-- BEFORE -->
<table>
  <tr><td>Product</td><td>Price</td><td>Stock</td></tr>
  <tr><td>Widget A</td><td>$19.99</td><td>In Stock</td></tr>
</table>

<!-- AFTER -->
<table>
  <caption>Product availability and pricing, October 2026</caption>
  <thead>
    <tr>
      <th scope="col">Product</th>
      <th scope="col">Price</th>
      <th scope="col">Stock status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Widget A</th>
      <td>$19.99</td>
      <td>In stock</td>
    </tr>
    <tr>
      <th scope="row">Widget B</th>
      <td>$29.99</td>
      <td>Out of stock</td>
    </tr>
  </tbody>
</table>
```
- **Positive note:** Stock status is conveyed in **text**, not colour alone — this correctly satisfies 1.4.1.
- **Responsive caution:** `width:100%` with `border-collapse` is fine, but ensure the table scrolls horizontally rather than being clipped at 320px (1.4.10). Wrap in `<div role="region" aria-labelledby="…" tabindex="0" style="overflow-x:auto">` so keyboard users can scroll it.

---

## 8. ARIA & Custom Widgets

### FINDING 8.1 — Wrong ARIA pattern for the country selector
- **Severity:** High
- **WCAG:** 4.1.2 Name, Role, Value (A), 1.3.1 (A)
- **Location:** The `role="button" aria-haspopup="true"` trigger + `role="menu"` / `role="menuitem"` list.
- **Issues:**
  1. **Role misuse.** `role="menu"` is for *application command menus* (like a desktop menu bar: Cut/Copy/Paste). Selecting a country from a list of values is a **select / combobox / listbox** pattern. Screen readers announce "menu, USA menu item 1 of 3", implying an action rather than a choice. Per APG, use `<select>` or a `combobox` + `listbox` with `aria-selected`.
  2. **No accessible name.** The trigger's name is "Select Country ▼" — the `▼` character is read literally ("black down-pointing triangle"). The `<p>Select your country:</p>` label is not associated with anything.
  3. **No `aria-controls`** linking trigger to the popup.
  4. **Roving tabindex missing.** All three `menuitem`s have `tabindex="0"`, so they are in the Tab sequence **even while the menu is hidden** — well, `display:none` removes them, but once open, Tab moves between items instead of the expected menu behaviour (Tab should close the menu and move on). APG requires `tabindex="-1"` on all items with a single `tabindex="0"`/roving focus.
  5. **Escape handled only on the items**, not on the trigger — pressing Escape while focused on the open trigger does nothing.
  6. **No outside-click / blur dismissal**, no `Home`/`End`/type-ahead support.
  7. **State is never reflected.** `selectCountry()` fires an `alert()` but never updates the trigger text or any form value, so the chosen value is not programmatically determinable and is not submitted with the form.
  8. `aria-expanded` is set from a JS boolean (`!isOpen`) — it stringifies correctly, but the state is derived from inline `style.display`, which breaks if the element is hidden by a class or media query.

**Recommended fix — use the native control:**
```html
<!-- AFTER (preferred) -->
<div class="field">
  <label for="country">Country</label>
  <select id="country" name="country" autocomplete="country-name">
    <option value="">Choose a country</option>
    <option value="US">United States</option>
    <option value="CA">Canada</option>
    <option value="MX">Mexico</option>
  </select>
</div>
```
Native `<select>` gives you: correct role and state, mobile OS pickers, type-ahead, form submission, Escape/Home/End, high-contrast-mode support, and zero JS.

**If a custom widget is mandated**, implement the APG *Select-Only Combobox*:
```html
<label id="country-label">Country</label>
<div id="country-combo" role="combobox" tabindex="0"
     aria-controls="country-listbox" aria-expanded="false"
     aria-labelledby="country-label country-combo"
     aria-activedescendant="">Choose a country</div>
<ul id="country-listbox" role="listbox" aria-labelledby="country-label" hidden>
  <li id="opt-us" role="option" aria-selected="false">United States</li>
  <li id="opt-ca" role="option" aria-selected="false">Canada</li>
  <li id="opt-mx" role="option" aria-selected="false">Mexico</li>
</ul>
<input type="hidden" name="country" id="country-value">
```
…with `aria-activedescendant` focus management, `Home`/`End`/type-ahead, `Escape` on the combobox, outside-click dismissal, and focus return to the combobox on selection.

- **User impact:** Screen reader users receive the wrong mental model and cannot tell which country is selected; the value never reaches the server; keyboard users hit unexpected Tab behaviour.

### FINDING 8.2 — Generic `div role="button"` with no visible focus style
- **Severity:** Medium
- **WCAG:** 2.4.7 Focus Visible (AA), 1.4.11 (AA), 4.1.2 (A)
- **Location:**
```html
<div tabindex="0" onclick="doSomething()" onkeydown="…" role="button"
     style="background: blue; color: white; padding: 10px; margin: 10px;">
```
- **Issues:**
  - Relies entirely on the UA default focus ring. On a saturated `blue` background the default ring in some browsers/themes drops below 3:1 contrast. Define an explicit `:focus-visible` indicator.
  - Same Space-key `keydown` auto-repeat issue as 5.4.
  - The accessible name is a 10-word sentence — button names should be short, action-oriented verb phrases (2.4.6).
  - In Windows High Contrast Mode, `background: blue` is discarded while the element provides no border — the control may vanish.

```html
<!-- AFTER -->
<button type="button" class="btn-secondary" onclick="doSomething()">
  Show details
</button>
```
```css
.btn-secondary{background:#0b57d0;color:#fff;border:2px solid transparent;padding:10px}
.btn-secondary:focus-visible{outline:3px solid #111;outline-offset:3px}
@media (forced-colors: active){ .btn-secondary{border-color: ButtonText} }
```

### FINDING 8.3 — `alert()` used for status messages
- **Severity:** Medium
- **WCAG:** 4.1.3 Status Messages (AA), 3.2.x
- **Location:** `submitForm()`, `selectCountry()`, `doSomething()`
- **Issue:** Native `alert()` steals focus, cannot be re-read, is suppressed in some embedded contexts, and provides no persistent record. Replace with an `aria-live="polite"` region (or `role="alert"` for errors) and manage focus deliberately after the action.

### FINDING 8.4 — No `prefers-reduced-motion` support
- **Severity:** Medium
- **WCAG:** 2.3.3 Animation from Interactions (AAA) — advisory; supports 2.2.2
- **Fix:**
```css
@media (prefers-reduced-motion: reduce){
  *, *::before, *::after{
    animation-duration:0.01ms !important;
    animation-iteration-count:1 !important;
    transition-duration:0.01ms !important;
    scroll-behavior:auto !important;
  }
}
```

---

## 9. Keyboard Navigation Summary

| Check | Result | Note |
|---|---|---|
| All functionality keyboard-operable (2.1.1) | ⚠️ Partial | Custom controls have handlers, but Space auto-repeats and form cannot be submitted by Enter from a text field |
| No keyboard trap (2.1.2) | ✅ Pass | Escape exits the menu; no traps detected |
| Focus order logical (2.4.3) | ⚠️ Partial | DOM order is logical; menu items enter the Tab sequence when open instead of using roving tabindex |
| Focus visible (2.4.7) | ⚠️ At risk | No author-defined indicators; defaults may fail 3:1 on blue/red backgrounds |
| Bypass blocks (2.4.1) | ⚠️ Partial | Skip link present and correctly styled, but target not focusable and no landmarks exist |
| Character key shortcuts (2.1.4) | ✅ N/A | None implemented |
| Focus returned after dismissal | ✅ Partial pass | Escape returns focus to trigger — good; selection does not |
| Pointer-only events | ❌ | `onclick` on `<div>`s; use real elements |

---

## 10. Prioritised Remediation Plan

**P0 — Blocking, fix immediately (est. 2 hours)**
1. Add `lang="en"`, `<meta charset>`, `<meta name="viewport">`.
2. Fix all contrast failures (body 2.2:1, callout 1.14:1, red button 4.0:1).
3. Add `alt` to the chart; empty `alt` on the decorative icon.
4. Label every form field with a real `<label for>`; delete placeholder-as-label.
5. Remove the infinite blink animation.
6. Add `controls`, remove `autoplay`/`loop` from the video.

**P1 — High (est. 1 day)**
7. Convert `div role="button"` → `<button>` (2 instances); delete the keyboard shims.
8. Replace the custom menu with `<select>`.
9. Add `<th scope>`, `<caption>`, `<thead>`/`<tbody>` to the table.
10. Rewrite link text; add `<main>` + headings `h1→h2`; add `tabindex="-1"` to the skip target.
11. Add captions/transcript for the video.

**P2 — Medium (est. 1 day)**
12. Implement validation with inline errors, an error summary, `aria-invalid`, and a polite live region; remove `alert()`.
13. Add `autocomplete` tokens.
14. Define `:focus-visible` styles at ≥3:1; add `forced-colors` support.
15. Add `prefers-reduced-motion` media query; replace 8px text with `rem` units.

---

## 11. Remediated Reference Implementation

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Widgets &amp; Contact – Acme Supply Co.</title>
<style>
  :root{ --ink:#1a1a1a; --bg:#fff; --brand:#00bbff; --primary:#0b57d0; --danger:#8a1c1c; }
  body{background:var(--bg);color:var(--ink);font-family:Arial,Helvetica,sans-serif;
       font-size:100%;line-height:1.5;margin:0}
  .container{max-width:70ch;margin:0 auto;padding:1.25rem}
  .banner{background:var(--brand);color:#000;padding:1rem}          /* 9.5:1 */
  .callout{background:#f0f0f0;color:var(--ink);padding:.75rem;border-left:4px solid var(--primary)}
  .fine-print{font-size:.875rem}
  .visually-hidden{position:absolute;width:1px;height:1px;margin:-1px;padding:0;
       overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}
  .skip-link{position:absolute;top:-60px;left:6px;background:#000;color:#fff;padding:.5rem;z-index:1000}
  .skip-link:focus{top:6px}
  :focus-visible{outline:3px solid var(--primary);outline-offset:3px}
  .btn{font:inherit;padding:.6rem 1.1rem;border:2px solid transparent;border-radius:4px;cursor:pointer}
  .btn-primary{background:#c00000;color:#fff}                        /* 5.9:1 */
  .btn-secondary{background:var(--primary);color:#fff}               /* 6.3:1 */
  .field{margin-block:1rem}
  label{display:block;font-weight:700;margin-bottom:.25rem}
  input,textarea,select{font:inherit;width:100%;padding:.5rem;
       border:2px solid #595959;background:#fff;color:var(--ink);border-radius:4px}
  .hint{font-size:.875rem;color:#595959;margin:.25rem 0 0}
  .error{color:var(--danger);font-weight:700;margin:.25rem 0 0}
  [aria-invalid="true"]{border-color:var(--danger)}
  table{border-collapse:collapse;width:100%}
  caption{text-align:left;font-weight:700;padding-bottom:.5rem}
  th,td{border:1px solid #595959;padding:.5rem;text-align:left}
  thead th{background:#eef2f7}
  .alert--urgent{background:var(--danger);color:#fff;border-left:6px solid #ffd400;padding:.75rem}
  @media (forced-colors: active){ .btn{border-color:ButtonText} }
  @media (prefers-reduced-motion: reduce){
    *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;
                         transition-duration:.01ms!important}
  }
</style>
</head>
<body>
<a href="#main-content" class="skip-link">Skip to main content</a>

<header class="banner">
  <p><strong>Acme Supply Co.</strong></p>
</header>

<main id="main-content" class="container" tabindex="-1">
  <h1>Welcome to Acme Supply Co.</h1>

  <div class="alert--urgent" role="alert">
    <strong>Urgent:</strong> Scheduled maintenance tonight from 10:00&nbsp;PM to 1:00&nbsp;AM&nbsp;ET.
  </div>

  <p class="callout">Free shipping on all orders over $50 this month.</p>

  <h2 id="chart-heading">Quarterly sales</h2>
  <figure>
    <img src="important-chart.jpg" width="300" height="200"
         alt="Bar chart of 2026 quarterly sales: Q1 $1.2M, Q2 $1.5M, Q3 $1.1M, Q4 $1.9M.">
    <figcaption>2026 quarterly sales. <a href="#inventory">See the product table below</a>.</figcaption>
  </figure>
  <img src="decorative-icon.png" alt="">

  <h2 id="inventory">Product availability</h2>
  <div role="region" aria-labelledby="inventory" tabindex="0" style="overflow-x:auto">
    <table>
      <caption>Product availability and pricing, October 2026</caption>
      <thead>
        <tr><th scope="col">Product</th><th scope="col">Price</th><th scope="col">Stock status</th></tr>
      </thead>
      <tbody>
        <tr><th scope="row">Widget A</th><td>$19.99</td><td>In stock</td></tr>
        <tr><th scope="row">Widget B</th><td>$29.99</td><td>Out of stock</td></tr>
      </tbody>
    </table>
  </div>

  <h2>Product video</h2>
  <video width="320" height="240" controls preload="metadata" poster="video-poster.jpg">
    <source src="background-video.mp4" type="video/mp4">
    <track kind="captions" src="captions-en.vtt" srclang="en" label="English" default>
    <track kind="descriptions" src="descriptions-en.vtt" srclang="en" label="English descriptions">
    <p>Your browser cannot play this video.
       <a href="transcript.html">Read the full transcript</a>.</p>
  </video>

  <h2 id="contact-heading">Contact us</h2>
  <div id="error-summary" role="alert" tabindex="-1" hidden>
    <h3>There is a problem with your submission</h3>
    <ul id="error-list"></ul>
  </div>

  <form id="contact-form" aria-labelledby="contact-heading" novalidate>
    <div class="field">
      <label for="name">Full name (required)</label>
      <input type="text" id="name" name="name" autocomplete="name"
             required aria-required="true" aria-describedby="name-hint">
      <p id="name-hint" class="hint">For example, Jane Smith.</p>
      <p id="name-err" class="error" hidden></p>
    </div>

    <div class="field">
      <label for="email">Email address (required)</label>
      <input type="email" id="email" name="email" autocomplete="email" required aria-required="true">
      <p id="email-err" class="error" hidden></p>
    </div>

    <div class="field">
      <label for="phone">Phone number <span class="hint">(optional)</span></label>
      <input type="tel" id="phone" name="phone" autocomplete="tel">
    </div>

    <div class="field">
      <label for="country">Country</label>
      <select id="country" name="country" autocomplete="country-name">
        <option value="">Choose a country</option>
        <option value="US">United States</option>
        <option value="CA">Canada</option>
        <option value="MX">Mexico</option>
      </select>
    </div>

    <div class="field">
      <label for="message">Message</label>
      <textarea id="message" name="message" rows="5"></textarea>
    </div>

    <button type="submit" class="btn btn-primary">Send message</button>
    <p id="form-status" role="status" aria-live="polite"></p>
  </form>

  <h2>More information</h2>
  <p>Read our <a href="info.html">product information guide</a> or see the
     <a href="details.html">detailed technical specifications</a>.</p>
  <p class="fine-print">Prices exclude tax and may change without notice.</p>

  <p><button type="button" class="btn btn-secondary" id="details-btn">Show shipping details</button></p>
  <div id="details-panel" hidden><p>Orders ship within two business days.</p></div>
</main>

<footer class="container"><p>&copy; 2026 Acme Supply Co.</p></footer>

<script>
(function(){
  var form = document.getElementById('contact-form');
  var summary = document.getElementById('error-summary');
  var list = document.getElementById('error-list');
  var status = document.getElementById('form-status');

  function clearError(input){
    var err = document.getElementById(input.id + '-err');
    if (err){ err.hidden = true; err.textContent = ''; }
    input.removeAttribute('aria-invalid');
  }
  function setError(input, msg){
    var err = document.getElementById(input.id + '-err');
    if (err){ err.textContent = msg; err.hidden = false; }
    input.setAttribute('aria-invalid','true');
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '#' + input.id; a.textContent = msg;
    li.appendChild(a); list.appendChild(li);
  }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    list.innerHTML = ''; summary.hidden = true; status.textContent = '';
    var fields = [document.getElementById('name'), document.getElementById('email')];
    fields.forEach(clearError);

    var name = fields[0], email = fields[1];
    if (!name.value.trim()) setError(name, 'Enter your full name.');
    if (!email.value.trim()) setError(email, 'Enter your email address.');
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value))
      setError(email, 'Enter an email address in the format name@example.com.');

    if (list.children.length){
      summary.hidden = false;
      summary.focus();            // move focus to the error summary (3.3.1)
    } else {
      status.textContent = 'Thank you. Your message has been sent.'; // 4.1.3
      form.reset();
    }
  });

  var btn = document.getElementById('details-btn');
  var panel = document.getElementById('details-panel');
  btn.setAttribute('aria-expanded','false');
  btn.setAttribute('aria-controls','details-panel');
  btn.addEventListener('click', function(){
    var open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    panel.hidden = open;
    btn.textContent = open ? 'Show shipping details' : 'Hide shipping details';
  });
})();
</script>
</body>
</html>
```

---

## 12. Verification Checklist

**Automated (catches ~30–40%)**
- axe DevTools / Lighthouse / IBM Equal Access — expect 0 violations after remediation.
- HTML validation via W3C Nu checker (catches missing `lang`, duplicate IDs, invalid nesting).

**Manual (required)**
1. **Keyboard only** — unplug the mouse. Tab through the entire page: every control reachable, visible focus at all times, Enter submits the form from a text field, Escape closes the select, no traps.
2. **Screen readers** — NVDA + Firefox, JAWS + Chrome, VoiceOver + Safari (desktop and iOS). Verify: landmark list, heading list (H1→H2 only), link list reads meaningfully out of context, every form field announces its label + required state + error.
3. **Contrast** — TPGi Colour Contrast Analyser on every text/background and UI-boundary pair; confirm ≥4.5:1 text and ≥3:1 non-text.
4. **Zoom/reflow** — 200% text-only zoom and 400% browser zoom at 1280×1024 (equals 320 CSS px); no horizontal scrolling of content, no clipping.
5. **Motion** — enable OS "Reduce motion"; confirm no looping animation and no autoplay.
6. **Forced colours** — Windows High Contrast Mode; confirm buttons and input borders remain visible.
7. **Speech input** — Dragon/Voice Control: say "click Send message" and "click Full name" and confirm the controls activate.

---

### Closing note
The single highest-leverage change in this document is to **stop re-creating native controls with `<div>` plus JavaScript**. Replacing the two `div[role=button]` elements and the custom menu with `<button>` and `<select>` removes roughly 70 lines of keyboard shim code and simultaneously resolves findings 5.4, 8.1, 8.2, and large parts of the keyboard and focus-visibility sections — with better results than any hand-rolled implementation.

---

## Analysis: accessibility-fixed-demo.html

# Accessibility Audit Report
## "Accessibility Best Practices Demo" — WCAG 2.1 Level AA Conformance Review

**Audit Date:** 9 October 2026
**Standard:** WCAG 2.1 Level AA / Section 508 (Revised 2017)
**Scope:** Single-page static HTML document with inline CSS and JavaScript

---

## 1. Executive Summary

This page is self-described as a "fixed" best-practices demo, and the structural foundation is genuinely strong: landmarks, heading order, table semantics, form labelling, and captions are all correctly implemented. However, the page is **not WCAG 2.1 AA conformant**. Several defects are hidden behind correct-looking markup — the classic "looks accessible to an automated scanner, fails for a real user" pattern.

| Severity | Count | Summary |
|---|---|---|
| **Critical** | 2 | Broken focus management on form submission; no accessible error handling/validation feedback |
| **High** | 5 | Skip link / in-page anchors don't move focus; missing `autocomplete`; conflicting `role="alert"` + `aria-live`; insufficient non-text contrast on form borders; no audio description/transcript for video |
| **Medium** | 6 | Focus indicator contrast failure; 3-second auto-dismissing alert; no `action` fallback (progressive enhancement); redundant `role="presentation"`; unnamed `<section>` landmarks; unused hover-only dropdown CSS |
| **Low** | 5 | Title/H1 mismatch; filler H3; fieldset scope; dead `.sr-only` code; instructional copy exposed to AT |

**Estimated conformance:** ~78% of applicable AA success criteria pass. The two Critical items block conformance with SC 3.3.1 and SC 2.4.3.

---

## 2. Critical Findings

---

### 🔴 CRITICAL-01 — Focus is silently lost on form submission

**WCAG:** 2.4.3 Focus Order (A), 4.1.3 Status Messages (AA), 3.3.1 Error Identification (A)
**Location:** `<script>` → `DOMContentLoaded` submit handler
**Severity:** Critical

#### Issue
The success handler calls `successDiv.focus()` on a `<div>` that has **no `tabindex` attribute**. Non-interactive elements are not focusable by default, so `.focus()` is a no-op. Focus remains on the submit button inside a form whose content has not changed.

Secondary problem: the element is created with **both** `role="alert"` and an attempted focus move. This is a known double-announcement anti-pattern — if focus *did* work, NVDA/JAWS would announce the live region *and* then the focused element.

Tertiary problem: the message is inserted **after** the form (`form.nextSibling`), meaning a keyboard user tabbing forward from the submit button lands in the footer and never encounters the confirmation in DOM order going backwards.

#### Before
```html
<script>
const successDiv = document.createElement('div');
successDiv.setAttribute('role', 'alert');
successDiv.setAttribute('aria-live', 'polite');
successDiv.textContent = 'Form submitted successfully! We will respond within 24 hours.';
form.parentNode.insertBefore(successDiv, form.nextSibling);
successDiv.focus(); // ← does nothing
</script>
```

#### After
```html
<!-- Persistent, pre-rendered status container ABOVE the form -->
<div id="form-status" role="status" aria-live="polite" tabindex="-1" class="status-region"></div>

<form id="contact" action="/contact" method="post" novalidate> … </form>

<script>
const form   = document.getElementById('contact');
const status = document.getElementById('form-status');

form.addEventListener('submit', function (e) {
  e.preventDefault();

  // ... run validation first (see CRITICAL-02) ...

  status.className = 'status-region status-success';
  status.innerHTML =
    '<h3>Message sent</h3><p>Form submitted successfully. We will respond within 24 hours.</p>';
  status.focus();          // works because tabindex="-1"
  form.reset();
});
</script>
```

**Key fixes:** container exists in the DOM *before* the event (reliable live-region announcement), `tabindex="-1"` makes it programmatically focusable, `role="status"` instead of `role="alert"` (polite is correct for success), and it sits *above* the form so forward tab order is logical.

#### User Impact
Screen reader users who submit the form may hear nothing at all (live regions injected in the same tick as their content are frequently missed by NVDA and VoiceOver). Keyboard-only and screen-magnifier users are left on a button at the bottom of the form while the confirmation renders off-screen below. Users cannot tell whether submission succeeded, and will re-submit repeatedly.

---

### 🔴 CRITICAL-02 — No accessible error identification, description, or suggestion

**WCAG:** 3.3.1 Error Identification (A), 3.3.3 Error Suggestion (AA), 1.4.1 Use of Color (A), 4.1.3 Status Messages (AA)
**Location:** `<form>` — all `<input>` / `<textarea>` elements
**Severity:** Critical

#### Issue
The form relies entirely on the browser's native `required` constraint bubbles. These bubbles:
- Are **not reliably announced** by all screen readers (Safari/VoiceOver support is poor, Firefox announces inconsistently).
- Auto-dismiss on a timer and cannot be re-summoned by keyboard.
- Cannot be styled, so they may fail contrast and text-spacing criteria.
- Only report **one error at a time**, forcing a tedious submit-fix-submit loop.

There is no `aria-invalid`, no `aria-describedby` pointing to an error message, no error summary, and no `role="alert"` error announcement. The `preventDefault()` in the submit handler means validation will never even surface in some flows.

#### Before
```html
<form>
  <div class="form-group">
    <label for="email">Email Address (required)</label>
    <input type="email" id="email" name="email" required aria-describedby="email-help">
    <small id="email-help">We'll use this to respond to your message</small>
  </div>
  <button type="submit" class="btn">Send Message</button>
</form>
```

#### After
```html
<div id="error-summary" tabindex="-1" role="alert" hidden class="error-summary">
  <h3>There is a problem</h3>
  <ul id="error-list"></ul>
</div>

<form id="contact" action="/contact" method="post" novalidate>
  <div class="form-group">
    <label for="email">Email address <span class="req">(required)</span></label>
    <input type="email" id="email" name="email"
           autocomplete="email"
           required aria-required="true"
           aria-describedby="email-help email-error"
           aria-invalid="false">
    <small id="email-help">We'll use this to respond to your message</small>
    <p id="email-error" class="field-error" hidden>
      <span aria-hidden="true">✖</span> Enter an email address in the format name@example.com
    </p>
  </div>
  <button type="submit" class="btn">Send message</button>
</form>
```

```js
function showError(input, message) {
  const err = document.getElementById(input.id + '-error');
  err.hidden = false;
  err.querySelector('.msg') && (err.querySelector('.msg').textContent = message);
  input.setAttribute('aria-invalid', 'true');
}
function clearError(input) {
  document.getElementById(input.id + '-error').hidden = true;
  input.setAttribute('aria-invalid', 'false');
}

form.addEventListener('submit', function (e) {
  e.preventDefault();
  const fields = form.querySelectorAll('[required], [type=email], [type=tel]');
  const errors = [];

  fields.forEach(f => {
    clearError(f);
    if (!f.checkValidity()) {
      showError(f, f.validationMessage);
      errors.push({ id: f.id, label: form.querySelector('label[for="'+f.id+'"]').textContent.trim() });
    }
  });

  const summary = document.getElementById('error-summary');
  if (errors.length) {
    document.getElementById('error-list').innerHTML = errors
      .map(err => `<li><a href="#${err.id}">${err.label}: please check this field</a></li>`).join('');
    summary.hidden = false;
    summary.focus();                 // moves AT + keyboard focus to the summary
    return;
  }
  summary.hidden = true;
  // ...success path (CRITICAL-01)...
});
```

**Critical CSS requirement (SC 1.4.1):** errors must not be signalled by red colour alone — the ✖ glyph, the error text, and `aria-invalid` all carry the meaning independently. Error text must meet 4.5:1; `#d32f2f` on white = 4.6:1 ✔ (avoid `#e74c3c`, which is only 3.5:1).

#### User Impact
Blind users receive no notification that submission failed, or hear a single untargeted browser bubble and assume the form is broken. Users with cognitive disabilities and dyslexia cannot recover from errors without explicit, persistent, plain-language suggestions. Colour-blind users cannot perceive red-only error styling. This is the single most common cause of abandoned transactions for disabled users.

---

## 3. High-Severity Findings

---

### 🟠 HIGH-01 — Skip link and in-page navigation do not move keyboard focus

**WCAG:** 2.4.1 Bypass Blocks (A), 2.4.3 Focus Order (A)
**Location:** `<a href="#main-content" class="skip-link">`, `<nav>` links to `#contact-form`, `#data-table`, `<main id="main-content">`

#### Issue
`<main>`, `<h2 id="contact-form">`, and `<h2 id="data-table">` are not focusable elements. In Chrome and Safari, activating a fragment link scrolls the viewport but **leaves keyboard focus on the link**. The next <kbd>Tab</kbd> press returns the user to the second nav item — the block they were trying to bypass. The skip link therefore fails its sole purpose in the most-used browsers.

Also note the `id` values are semantically misleading: `contact-form` is on a heading, not the `<form>`; `data-table` is on a heading, not the `<table>`.

#### Before
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
...
<main id="main-content" class="container">
...
<h2 id="contact-form">Accessible Contact Form</h2>
<h2 id="data-table">Product Information</h2>
```

#### After
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
...
<main id="main-content" class="container" tabindex="-1">
...
<section aria-labelledby="contact-heading">
  <h2 id="contact-heading" tabindex="-1">Accessible contact form</h2>
```
```html
<nav aria-label="Main">
  <ul>
    <li><a href="#main-content">Home</a></li>
    <li><a href="#contact-heading">Contact</a></li>
    <li><a href="#products-heading">Products</a></li>
  </ul>
</nav>
```
```css
/* Suppress the focus ring on programmatic-only targets */
main:focus, h2[tabindex="-1"]:focus { outline: none; }
main:focus-visible { outline: 3px solid #0056b3; } /* still visible if truly tabbed to */
```

#### User Impact
Keyboard-only users (motor impairments, RSI, switch users) and screen reader users cannot bypass the repeated navigation block. On a page with many nav items this is a measurable fatigue and time cost on every page load.

---

### 🟠 HIGH-02 — Missing `autocomplete` attributes on personal-data inputs

**WCAG:** 1.3.5 Identify Input Purpose (AA) — **direct AA failure**
**Location:** `#name`, `#email`, `#phone`

#### Issue
WCAG 2.1 added SC 1.3.5 specifically for AA. Any input collecting information *about the user* that matches the HTML autofill taxonomy **must** carry the correct `autocomplete` token. All three fields here qualify and none have it.

#### Before
```html
<input type="text"  id="name"  name="name"  required aria-describedby="name-help">
<input type="email" id="email" name="email" required aria-describedby="email-help">
<input type="tel"   id="phone" name="phone"         aria-describedby="phone-help">
```

#### After
```html
<input type="text"  id="name"  name="name"  autocomplete="name"  required aria-describedby="name-help">
<input type="email" id="email" name="email" autocomplete="email" required aria-describedby="email-help">
<input type="tel"   id="phone" name="phone" autocomplete="tel"            aria-describedby="phone-help">
```

#### User Impact
Users with motor impairments cannot leverage browser/password-manager autofill, forcing error-prone manual entry. Users with cognitive disabilities and memory impairments lose the ability to have assistive tech substitute familiar symbols/icons for field purposes. Users with dyslexia lose autofill as a spelling safeguard.

---

### 🟠 HIGH-03 — Conflicting `role="alert"` with `aria-live="polite"` on static content

**WCAG:** 4.1.2 Name, Role, Value (A), 4.1.3 Status Messages (AA)
**Location:** `<div role="alert" aria-live="polite">` in the "Important Notice" section

#### Issue
Two distinct defects:
1. **Contradictory ARIA.** `role="alert"` has an implicit `aria-live="assertive"`. Explicitly setting `aria-live="polite"` creates an undefined-behaviour conflict; NVDA honours the explicit value, JAWS and VoiceOver behave inconsistently.
2. **Live region on static content.** This content is present at page load and never changes. A live region is only for *dynamically inserted or updated* content. Some screen readers announce `role="alert"` regions on page load, interrupting the document title/landmark announcement with content the user hasn't navigated to. The content is also then announced a *second* time when the user reaches it in reading order.

#### Before
```html
<div role="alert" aria-live="polite">
  <p><strong>Notice:</strong> This important message is delivered without blinking…</p>
</div>
```

#### After
```html
<!-- Static advisory content: no live region needed -->
<div class="notice">
  <p><strong>Notice:</strong> This important message is delivered without blinking or
     auto-updating content that could cause seizures.</p>
</div>
```
```html
<!-- If you genuinely need a dynamic alert, pick ONE of: -->
<div role="alert"></div>                     <!-- urgent, interrupts -->
<div role="status" aria-live="polite"></div> <!-- non-urgent, queues -->
```

**Rule of thumb:** never pair `role="alert"` with `aria-live`; never put a live role on markup that is static at load time.

#### User Impact
Screen reader users experience an unsolicited interruption during the critical page-load orientation phase, then hear duplicate content. For users with cognitive disabilities, duplicated and out-of-context announcements significantly increase comprehension load.

---

### 🟠 HIGH-04 — Form control borders fail non-text contrast

**WCAG:** 1.4.11 Non-text Contrast (AA)
**Location:** `input, textarea, select { border: 2px solid #ddd; }`

#### Issue
The only visual boundary of each form field is a `#dddddd` border on the `#ffffff` page background. Contrast ratio = **1.30:1**. SC 1.4.11 requires **3:1** for visual information needed to identify a user-interface component and its boundary.

The `.btn` is fine (white on `#0056b3` = 7.0:1 text, and the button has a solid fill). The `<table>` borders are also `#ddd` but the cells are identified by their text content, so that is advisory rather than a failure.

#### Before
```css
input, textarea, select {
  border: 2px solid #ddd;   /* 1.30:1 against #fff — FAIL */
}
```

#### After
```css
input, textarea, select {
  border: 2px solid #6c757d;   /* 4.68:1 against #fff — PASS */
  background-color: #fff;
}
input[aria-invalid="true"],
textarea[aria-invalid="true"] {
  border-color: #d32f2f;        /* 4.6:1 — plus icon + text per 1.4.1 */
  border-width: 3px;
}
```

#### User Impact
Users with low vision, cataracts, or contrast sensitivity loss cannot determine where a text field begins and ends, or distinguish an input from surrounding static text. This also affects all users on low-quality displays or in high ambient light.

---

### 🟠 HIGH-05 — Video lacks audio description and transcript

**WCAG:** 1.2.3 Audio Description or Media Alternative (A), 1.2.5 Audio Description (AA), 1.2.2 Captions (A)
**Location:** `<video>` element

#### Issue
The `<video>` has a captions `<track>`, which addresses SC 1.2.2 for deaf/hard-of-hearing users *provided* `captions.vtt` is a real, synchronised, verbatim file including speaker identification and non-speech audio. It does **not** address blind users:
- **No audio description** track or described version (fails AA SC 1.2.5).
- **No text transcript** (the most robust alternative, and the only one usable by deafblind users with a braille display).

The `aria-describedby` paragraph — "This video demonstrates our product features with captions available" — is a *description of the player*, not a media alternative, and does not satisfy any media success criterion.

Additionally, `<track>` ordering is correct (after `<source>`), but there is no `default` attribute and no second `kind="descriptions"` track.

#### Before
```html
<video width="320" height="240" controls aria-describedby="video-description">
  <source src="background-video.mp4" type="video/mp4">
  <track kind="captions" src="captions.vtt" srclang="en" label="English captions">
  Your browser does not support the video tag.
</video>
<p id="video-description">This video demonstrates our product features with captions available.</p>
```

#### After
```html
<figure>
  <video width="640" height="360" controls preload="metadata"
         poster="product-poster.jpg" aria-label="Product feature overview">
    <source src="product-overview.mp4" type="video/mp4">
    <source src="product-overview.webm" type="video/webm">
    <track kind="captions" src="captions-en.vtt" srclang="en" label="English" default>
    <track kind="descriptions" src="descriptions-en.vtt" srclang="en" label="English audio descriptions">
    <p>Your browser does not support HTML video.
       <a href="product-overview.mp4">Download the video (MP4, 24 MB)</a>.</p>
  </video>

  <figcaption>Product feature overview (3 min 42 s).</figcaption>
</figure>

<details>
  <summary>Read the full transcript of “Product feature overview”</summary>
  <div>
    <p><strong>Narrator:</strong> …</p>
    <p><em>[On screen: dashboard showing a 25% quarterly increase]</em></p>
  </div>
</details>
<p><a href="product-overview-described.mp4">Watch the audio-described version</a></p>
```

Also note: `width="320" height="240"` renders captions at an unusably small size. A minimum rendered width of ~480 px is recommended for legible caption text; ensure the player is responsive (`max-width: 100%; height: auto;`).

#### User Impact
Blind and low-vision users cannot access any visual-only information in the video (on-screen text, demonstrated gestures, charts). Deafblind users have no access at all without a transcript. Users with cognitive disabilities and non-native speakers lose the transcript as a scannable, searchable alternative.

---

## 4. Medium-Severity Findings

---

### 🟡 MEDIUM-01 — Button focus indicator fails contrast against the page background

**WCAG:** 1.4.11 Non-text Contrast (AA), 2.4.7 Focus Visible (AA)
**Location:** `.btn:focus { outline: 3px solid #80bdff; outline-offset: 2px; }`

Because `outline-offset: 2px` lifts the ring off the dark button and onto the white page background, the relevant contrast pair is `#80bdff` vs `#ffffff` = **1.96:1** (requires 3:1). Also, `:focus` applies the ring on mouse click as well as keyboard.

**After:**
```css
.btn:focus { outline: none; }                  /* reset only */
.btn:focus-visible {
  outline: 3px solid #0b3d91;                  /* 10.2:1 vs white, 2.3:1 vs button… */
  outline-offset: 3px;
  box-shadow: 0 0 0 6px #ffffff, 0 0 0 9px #0b3d91; /* dual-tone ring: visible on any bg */
}
a:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible {
  outline: 3px solid #0b3d91;
  outline-offset: 2px;
}
@media (forced-colors: active) {
  .btn:focus-visible { outline: 3px solid Highlight; }
}
```
Use a **dual-tone (white + dark) ring** so the indicator passes on both light and dark surfaces — this is the WCAG 2.2 "Focus Appearance" technique and is the most future-proof approach.

The fields' focus style (`outline: none` + `border-color` + `box-shadow`) technically passes once HIGH-04 is fixed, but currently the *change* from `#ddd` to `#007bff` is the only cue; after the fix (`#6c757d` → `#0b3d91`) verify the indicator-vs-unfocused-state contrast is ≥ 3:1.

**Impact:** Low-vision and keyboard users lose track of their position on the page.

---

### 🟡 MEDIUM-02 — Status message auto-dismisses after 3 seconds

**WCAG:** 2.2.1 Timing Adjustable (A), 4.1.3 Status Messages (AA)
**Location:** `showMessage()` → `setTimeout(..., 3000)`

The toast is removed after 3 s with no way to extend, pause, or dismiss it, and no persistent record of it. This is a non-essential time limit with no exception under SC 2.2.1. Three seconds is well below the time a screen magnifier user needs to locate an element in the top-right corner, and a screen reader user who is mid-announcement may have the node removed before the live region finishes reading.

**After:**
```html
<div id="toast-region" role="status" aria-live="polite" class="toast-region"></div>
```
```js
let toastTimer;
function showMessage() {
  const region = document.getElementById('toast-region');
  region.innerHTML = '';

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = '<p>Button activated successfully.</p>';

  const close = document.createElement('button');
  close.type = 'button';
  close.textContent = 'Dismiss';
  close.addEventListener('click', () => { region.innerHTML = ''; });
  toast.appendChild(close);
  region.appendChild(toast);

  // Persist indefinitely for reduced-motion / AT users; otherwise 20s minimum
  const persist = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  clearTimeout(toastTimer);
  if (!persist) toastTimer = setTimeout(() => { region.innerHTML = ''; }, 20000);

  // Pause the dismissal while the user is interacting with the toast
  toast.addEventListener('mouseenter', () => clearTimeout(toastTimer));
  toast.addEventListener('focusin',   () => clearTimeout(toastTimer));
}
```
Also note the toast uses `position: fixed` at `top: 20px; right: 20px` — at 400% zoom (SC 1.4.10 Reflow) this can overlay and permanently obscure page content. Constrain with `max-width: calc(100vw - 40px)`.

---

### 🟡 MEDIUM-03 — No server-side fallback (progressive enhancement failure)

**WCAG:** 4.1.1 / general robustness; Section 508 §501
**Location:** `<form>` (no `action`, no `method`), `onclick="showMessage()"`

The form has no `action` or `method` attribute and is entirely dependent on `preventDefault()`. If the script fails to load, is blocked by a corporate proxy, or errors earlier in execution, the form silently does nothing when submitted — with no error. Users on assistive technologies are disproportionately affected by script failures (older AT/browser combinations, restricted enterprise environments).

**After:**
```html
<form id="contact" action="/api/contact" method="post" novalidate>
```
Enhance with JS; degrade to a full page POST without it. Likewise, replace the inline `onclick` with an attached listener so behaviour is centralised and CSP-compatible:
```js
document.getElementById('demo-button')
        .addEventListener('click', showMessage);
```

---

### 🟡 MEDIUM-04 — Redundant / conflicting ARIA on the decorative image

**WCAG:** 1.1.1 Non-text Content (A) — advisory
**Location:** `<img src="decorative-icon.png" alt="" role="presentation">`

`alt=""` already removes the image from the accessibility tree. Adding `role="presentation"` is redundant, and in some older AT builds the explicit role plus a `width`/`height` can produce an unlabeled graphic node. Follow the **first rule of ARIA**: don't use ARIA when native HTML already does the job.

**Before:** `<img src="decorative-icon.png" alt="" role="presentation">`
**After:** `<img src="decorative-icon.png" alt="" width="32" height="32">`

Better still, if it is purely ornamental, move it to CSS (`background-image`) so it never enters the DOM.

Separately — the `alt` on the chart image ("Sales chart showing 25% increase in Q4 2024") is good, but a chart is a **complex image** (SC 1.1.1 + G92). A single sentence cannot convey the underlying data. Provide a long description:
```html
<figure>
  <img src="important-chart.jpg" alt="Bar chart of quarterly sales for 2024. Full data in the table below."
       width="300" height="200">
  <figcaption id="chart-desc">
    Quarterly sales 2024: Q1 $1.2M, Q2 $1.4M, Q3 $1.6M, Q4 $2.0M — a 25% increase from Q3 to Q4.
  </figcaption>
</figure>
```

---

### 🟡 MEDIUM-05 — `<section>` elements have no accessible name

**WCAG:** 1.3.1 Info and Relationships (A) — advisory / best practice
**Location:** all nine `<section>` elements

A `<section>` without an accessible name is **not exposed as a `region` landmark**. The nine sections therefore contribute nothing to landmark navigation — screen reader users see only `banner`, `navigation`, `main`, `contentinfo`. Either name them or let the headings do the work.

**After:**
```html
<section aria-labelledby="products-heading">
  <h2 id="products-heading">Product information</h2>
  …
</section>
```
This creates navigable regions named after their headings and, as a bonus, supplies stable anchor targets for the nav links (see HIGH-01).

---

### 🟡 MEDIUM-06 — Hover-only dropdown CSS is a keyboard trap waiting to happen

**WCAG:** 2.1.1 Keyboard (A), 1.4.13 Content on Hover or Focus (AA)
**Location:** `.dropdown` / `.dropdown-content` CSS rules (currently unused)

The stylesheet ships a dropdown pattern with `display: none` and a `:hover` reveal on the child links only. Because the *container* is never shown on focus, tabbing into the menu would move focus to invisible links. There is also no dismiss mechanism (SC 1.4.13 requires hoverable, dismissible, persistent).

Either delete the dead CSS, or implement the disclosure pattern correctly:
```html
<div class="dropdown">
  <button type="button" id="menu-btn" aria-expanded="false" aria-controls="menu-list">
    Products <span aria-hidden="true">▾</span>
  </button>
  <ul id="menu-list" class="dropdown-content" hidden>
    <li><a href="/widgets">Widgets</a></li>
    <li><a href="/gadgets">Gadgets</a></li>
  </ul>
</div>
```
```css
.dropdown-content[hidden] { display: none; }
.dropdown-content { display: block; }           /* visibility driven by [hidden], not :hover */
```
```js
btn.addEventListener('click', () => {
  const open = btn.getAttribute('aria-expanded') === 'true';
  btn.setAttribute('aria-expanded', String(!open));
  list.hidden = open;
});
document.addEventListener('keydown', e => {   // 1.4.13 dismissible
  if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
    btn.setAttribute('aria-expanded','false'); list.hidden = true; btn.focus();
  }
});
```

---

## 5. Low-Severity Findings

| ID | WCAG | Issue | Fix |
|---|---|---|---|
| **LOW-01** | 2.4.2 Page Titled (A) | `<title>` is "Accessibility Issues Fixed - Best Practices Demo" but `<h1>` is "Accessibility Best Practices Demo". Mismatched titles disorient screen reader users who navigate by tab/window title, and hurt voice-control users saying the page name. | Align them: `<title>Accessibility Best Practices Demo | Example Co.</title>` — unique page name first, site name last. |
| **LOW-02** | 1.3.1 / 2.4.6 | `<h3>This heading order follows proper hierarchy</h3>` is meta-commentary, not a content heading. Headings must describe the section they introduce (SC 2.4.6 Headings and Labels). It pollutes the heading-list navigation. | Remove it, or replace with a descriptive heading for the content that follows. Likewise the `<p><em>Note: Decorative images should have empty alt text…</em></p>` is author commentary exposed to all users. |
| **LOW-03** | 1.3.1 | The `<fieldset>`/`<legend>` wraps the *entire* form including the submit button. `<fieldset>` is intended to group **related** controls (e.g. a radio group, or an address block). Every control's accessible name is now prefixed with "Contact Information" on JAWS, adding verbosity. | Either drop the fieldset (a single-purpose form with a heading doesn't need one) or scope it to a genuine sub-group and move the button outside it. |
| **LOW-04** | — | `.sr-only` class is defined but never used; `.dropdown` CSS is unused. Dead code invites future misuse. | Remove, or actually use `.sr-only` (e.g. for the "(required)" indicator or a "opens in new tab" hint). Note: the `.sr-only` implementation is otherwise correct — it includes `white-space: nowrap`, which prevents the classic single-character-per-line bug. |
| **LOW-05** | 1.4.4 / 1.4.12 | Hint text uses `<small>`, which computes to ~12.8 px. While `#333` on white passes contrast, sub-14 px hint text is a known readability barrier. `<small>` also carries "side comment / fine print" semantics that are inappropriate for required instructions. | Use `<p class="hint">` with `font-size: 0.9375rem` (15 px) minimum. Verify the layout survives SC 1.4.12 Text Spacing (line-height 1.5×, letter-spacing 0.12em, word-spacing 0.16em, paragraph-spacing 2×). |

---

## 6. What the Page Does Well ✅

Credit where it's due — these are correctly implemented and should be preserved:

| Area | Implementation |
|---|---|
| **Document structure** | `<!DOCTYPE html>`, `lang="en"`, `charset` declared first, no `user-scalable=no` or `maximum-scale` on the viewport (SC 1.4.4 ✔) |
| **Landmarks** | `<header>`, `<nav>`, `<main>`, `<footer>` all top-level → correct `banner`/`navigation`/`main`/`contentinfo` roles |
| **Nav labelling** | `aria-label="Main navigation"` on `<nav>` — though drop the word "navigation" (AT already announces the role, producing "main navigation navigation") → use `aria-label="Main"` |
| **Heading hierarchy** | Single `<h1>`, no skipped levels — SC 1.3.1 and 2.4.10 ✔ |
| **Data table** | `<caption>`, `<thead>`/`<tbody>`, `scope="col"` and `scope="row"` with row headers as `<th>` — exemplary SC 1.3.1 implementation |
| **Link text** | All links are self-describing out of context ("Read our detailed service information" not "click here") — SC 2.4.4 ✔ |
| **Native controls** | Real `<button type="submit">`, real `<select>`, real `<label for>` — no `div` buttons, no custom listbox. Maximum compatibility, zero ARIA needed. |
| **Body text contrast** | `#333` on `#fff` = **12.63:1**; `.good-contrast` `#333` on `#f8f9fa` = **12.1:1**; `.btn` white on `#0056b3` = **7.0:1**, hover `#003d82` = **11.0:1** — all comfortably exceed AA and most exceed AAA |
| **Skip link styling** | Correct off-screen-until-focused pattern with `top: -40px` → `top: 6px` on `:focus` (a real link, not `display: none`, so it's reachable) |
| **No seizure risk** | No blinking, flashing, autoplay, or auto-refresh — SC 2.3.1 and 2.2.2 ✔ |
| **Video** | `controls` present, no `autoplay`, captions track supplied, text fallback inside the element |
| **Form field types** | `type="email"` and `type="tel"` trigger appropriate mobile keyboards — a genuine cognitive/motor win |

---

## 7. Prioritised Remediation Roadmap

**Sprint 1 — Blocks conformance (do first)**
1. CRITICAL-02: Build the full validation/error pattern (error summary + inline errors + `aria-invalid`).
2. CRITICAL-01: Rewrite the success path — pre-rendered `role="status"` container, `tabindex="-1"`, placed before the form.
3. HIGH-01: Add `tabindex="-1"` to `#main-content` and all in-page anchor targets; retarget nav links.
4. HIGH-02: Add `autocomplete` to the three personal-data fields. *(5-minute fix, outsized value.)*

**Sprint 2 — High-impact UX**
5. HIGH-04 + MEDIUM-01: Contrast pass on form borders and focus rings; adopt `:focus-visible` with a dual-tone indicator and a `forced-colors` fallback.
6. HIGH-03: Remove the live region from the static notice; standardise on one live-region pattern site-wide.
7. HIGH-05: Commission transcript + audio-described version; add `kind="descriptions"` track and `default` on captions.

**Sprint 3 — Hardening & polish**
8. MEDIUM-02: Replace the 3-second toast with a dismissible, 20-second-minimum status region.
9. MEDIUM-03: Add `action`/`method`; move inline `onclick` to an event listener.
10. MEDIUM-04/05/06 and all LOW items; delete dead CSS.

---

## 8. Verification Checklist

Automated tools will catch perhaps 3 of the 18 issues above. Manual testing is mandatory.

**Automated (baseline only)**
- [ ] axe DevTools — expect 0 violations *after* remediation
- [ ] WAVE — check structure/landmark panel
- [ ] HTML validator (nu) — duplicate IDs, invalid nesting, orphaned `for` attributes
- [ ] Lighthouse accessibility score ≥ 95 (necessary, not sufficient)

**Manual keyboard**
- [ ] <kbd>Tab</kbd> from the URL bar: first stop is the skip link, it is visible, and activating it places focus in `<main>` (verify by pressing <kbd>Tab</kbd> again — you must land on the first link *inside* main)
- [ ] Every interactive element reachable; focus indicator visible on every one, against both light and dark surfaces
- [ ] No keyboard trap; <kbd>Esc</kbd> dismisses the toast
- [ ] Submit the empty form by keyboard — focus must land on the error summary; each summary link must jump focus to the corresponding field
- [ ] Video: <kbd>Space</kbd>/arrow keys operate the player; caption menu is keyboard reachable

**Screen readers (test at least two)**
- [ ] NVDA + Firefox, JAWS + Chrome, VoiceOver + Safari (macOS and iOS)
- [ ] Form mode: labels, hints, required state, and error text all announced on field entry
- [ ] Submit success/failure announced exactly once, with no interruption on page load
- [ ] Table: row/column headers announced when navigating with <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+arrows
- [ ] Landmark list (<kbd>D</kbd> in NVDA) and heading list (<kbd>H</kbd>) are meaningful

**Visual / low vision**
- [ ] 400% browser zoom at 1280×1024 → no horizontal scroll, no content obscured by the fixed toast (SC 1.4.10)
- [ ] Text-spacing bookmarklet applied → no clipping or overlap (SC 1.4.12)
- [ ] Windows High Contrast Mode / `forced-colors: active` → focus rings and borders still visible
- [ ] Greyscale filter → error states still distinguishable (SC 1.4.1)
- [ ] Contrast analyser on every foreground/background pair, including focus rings and field borders

**Cognitive / robustness**
- [ ] Disable JavaScript → form still submits to the server
- [ ] Reading level of error messages ≤ lower secondary education
- [ ] `prefers-reduced-motion` respected for the `.btn` transition and toast animation

---

### Closing note
The gap between this page and genuine conformance is instructive: every remaining defect lives in the **behavioural layer** — focus movement, error communication, live-region timing — rather than in the static markup. Automated scanners and markup-only reviews consistently miss exactly these issues, which is why keyboard-and-screen-reader walkthroughs of each user flow must be part of your definition of done.

---

