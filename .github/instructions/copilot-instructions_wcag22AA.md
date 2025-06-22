---
applyTo: '**'
---
# Copilot Code Review Custom Instructions

When reviewing pull requests:
- Only check for WCAG 2.2 Level AA accessibility compliance.
- Focus on content structure: proper semantic HTML (headings, landmarks).
- Ensure all functionality is operable via keyboard only.
- Verify color contrast ratios: ≥4.5:1 for normal text, ≥3:1 for large text and UI components.
- Check for appropriate ARIA usage and accessible names/roles.
- Confirm form controls have associated labels and clear error handling.
- Validate focus order and visible focus indicators.
- Do not comment on unrelated code quality, style, or performance issues.
