# Accessibility Demo - Learning Guide

![image](image.png)

Learn web accessibility through two HTML files: one with common accessibility problems and another showing the fixes. Perfect for developers learning WCAG 2.1 AA compliance.

> **⚡ Quick Start:** Want a hands-on walkthrough? Check out **[demo.md](demo.md)** for a streamlined IDE & browser-only tutorial that gets you from broken to fixed accessibility in minutes.

## Prerequisites

- VS Code with GitHub Copilot
- Chrome/Edge browser
- Install these extensions:
  - [Accessibility Insights for Web](https://accessibilityinsights.io/)
  - [Axe Linter for VS Code](https://marketplace.visualstudio.com/items?itemName=deque-systems.vscode-axe-linter)

## Quick Demo Flow

### 1. Get the Code (1 min)
```
1. Go to https://github.com/roryp/accessibilitydemo
2. Click "Fork" → "Create fork"
3. In VS Code: File → Clone Repository → paste your fork URL
```

### 2. See the Problems (2 min)
1. Open `accessibility-issues-demo.html` in VS Code
2. Look at the Problems panel - Axe Linter shows issues in real-time
3. Right-click the file → "Open with Live Server" (or just open in browser)
4. Run Accessibility Insights FastPass to see a full report

### 3. Fix with AI (3 min)
Open Copilot Chat (Ctrl+Alt+I) and paste:
```
Fix all accessibility issues in accessibility-issues-demo.html to meet WCAG 2.1 AA standards
```
Review → Accept → Save

### 4. Verify Success (2 min)
1. Commit and push your changes
2. Create a Pull Request
3. Watch the automated checks pass ✅

## What Just Happened?

You fixed 13+ accessibility violations:
- ❌ Poor color contrast → ✅ WCAG compliant colors
- ❌ Missing alt text → ✅ Descriptive image labels  
- ❌ Wrong heading order → ✅ Proper H1→H2→H3 hierarchy
- ❌ Unlabeled forms → ✅ Accessible form controls
- And 9 more issues...

## 🧪 Testing Tools

### Manual Testing
- **Keyboard**: Tab through both demos
- **Screen Reader**: Use NVDA, JAWS, or VoiceOver
- **Browser Tools**: Chrome DevTools Lighthouse

### Automated Tools
- **Accessibility Insights** - [Download here](https://accessibilityinsights.io/downloads)
- **axe DevTools** - Browser extension
- **WAVE** - Web accessibility evaluation
- **Lighthouse** - Built into Chrome

## 🚀 Automated Testing Workflows

Three CI/CD workflows run on every push and PR:

### 1. axe-core Testing
- Tests both HTML files automatically
- Generates detailed violation reports
- Fails builds for serious violations in fixed demo

### 2. Pa11y Testing  
- Command-line accessibility testing
- WCAG2AA standard compliance
- Comments results on pull requests

### 3. AI-Powered Analysis
- Uses GPT-4.1 via GitHub Models
- Comprehensive WCAG 2.1 AA analysis
- Detailed remediation guidance

### Local Testing Commands
```bash
# axe-core
npm install --save-dev @axe-core/cli serve
npx serve . -l 3000 &
npx axe http://localhost:3000/accessibility-issues-demo.html

# Pa11y
npm install -g pa11y-ci
python -m http.server 8080
pa11y http://localhost:8080/accessibility-issues-demo.html --standard WCAG2AA

# AI Analysis (requires MODELS_TOKEN)
pip install requests
python ai_accessibility_analyzer.py
```

## 🤖 AI-Assisted Development

### Copilot Instructions
This repository includes custom instructions to ensure consistent accessibility-focused development:

- **`.github/instructions/copilot-instructions.md`** - Custom instructions for GitHub Copilot
  - Focuses on WCAG 2.2 Level AA compliance during code generation
  - Ensures semantic HTML structure and proper accessibility patterns
  - Guides Copilot to prioritize keyboard navigation and ARIA usage

- **PR Review Instructions** - Automated accessibility checks in pull requests
  - Only reviews for WCAG 2.2 Level AA accessibility compliance
  - Validates semantic HTML, keyboard operability, and color contrast
  - Checks ARIA usage, form labels, and focus management
  - Ignores unrelated code quality issues to focus purely on accessibility

### GitHub Copilot Prompts
```
Fix color contrast issues to meet WCAG AA standards
Add proper alt text to all images  
Correct heading hierarchy starting with h1
Make form fields properly labeled with semantic elements
```

### Working with Issues
```bash
@github Create issue for missing alt text in accessibility-issues-demo.html
@github Start working on issue #123 about alt text
@github Fix contrast issues to meet WCAG 2.1 AA standards
```

## 🤖 AI Analysis Setup

Quick setup for GPT-4.1 accessibility analysis:

### 1. Get GitHub Models Access
- Visit [GitHub Models](https://github.com/marketplace/models)
- Sign in with your GitHub account
- Test models directly in the interface

### 2. Configure Repository Secrets
1. **Create Personal Access Token**:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
   - Create token with `Models` scope enabled
   - Copy the token value

2. **Add Repository Secret**:
   - Navigate to repository Settings → Secrets and variables → Actions
   - Click **New repository secret**
   - Name: `MODELS_TOKEN`
   - Value: Paste your token
   - Click **Add secret**

### 3. Run the Analysis
The AI checker runs automatically on pushes and pull requests, or manually via Actions tab.

### Sample AI Output
```markdown
## Accessibility Issue: Missing Alt Text
- **Severity**: High
- **WCAG Guideline**: 1.1.1 Non-text Content
- **Issue**: <img src="logo.png"> lacks alternative text
- **Remediation**: Add alt attribute: <img src="logo.png" alt="Company Logo">
- **User Impact**: Screen reader users cannot understand image content
```

## 📋 WCAG Guidelines

- **Level A**: Minimum accessibility
- **Level AA**: Standard level (recommended)  
- **Level AAA**: Highest level (government/critical services)

Target **WCAG 2.1 AA** for best balance of accessibility and practicality.

## 📚 Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM](https://webaim.org/) - Practical resources and tools
- [A11y Project](https://www.a11yproject.com/) - Community checklist
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)

## Next Steps
- Compare your fixes with `accessibility-fixed-demo.html`
- Run the AI analyzer locally: `python ai_accessibility_analyzer.py`
- Explore the GitHub Actions workflows that ran automatically

---

### How This Was Created

Generated with AI using this prompt:
```
create a simple html file to showcase how to fix accessibility issues. make the page deliberately non accessibility with a few issues. use plain html
```

**Result**: Two HTML files, 13+ accessibility patterns, automated testing workflows, and comprehensive learning guide.