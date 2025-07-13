# Accessibility Demo - IDE & Browser-Only Walk-through

![image](image.png)

Move the **[accessibilitydemo](https://github.com/roryp/accessibilitydemo)** repository from failing WCAG checks to full compliance without touching a terminal—everything happens in your **browser** or **VS Code**.

> **Flow:** Manual discovery → Semi-AI fixes → Full-AI agent → CI validation

## Prerequisites

- VS Code with GitHub Copilot
- Chrome/Edge browser
- Install these extensions:
  - [Accessibility Insights for Web](https://accessibilityinsights.io/)
  - [Axe Linter for VS Code](https://marketplace.visualstudio.com/items?itemName=deque-systems.vscode-axe-linter)

## Complete Demo Flow

### 1. Setup (UI only)
1. **Fork** the repository on GitHub
2. In VS Code choose **File → Clone Repository** and paste the URL of **your fork**
3. Open the workspace and choose **Trust** when prompted

### 2. Initial Testing - Accessibility Insights & Axe Linter
1. Open **`accessibility-issues-demo.html`** in Chrome/Edge
2. Click the **Accessibility Insights for Web** extension icon
3. Run a **FastPass** to capture an automated + tab stops report
4. In VS Code, check the **Problems** panel for Axe Linter issues

### 3. Semi-AI Fixes with Copilot Completions
1. Add guiding comments like `<!-- TODO: add alt text -->` and press **Tab**
2. Stage changes and commit through Source Control panel

### 4. Full AI Fixes with Copilot Agent
1. Open **Copilot Chat** (Ctrl+Alt+I)
2. Prompt:
   ```
   Fix all accessibility issues in accessibility-issues-demo.html to meet WCAG 2.1 AA standards. 
   Address color contrast, semantic structure, headings, labels, alt text, focus management, 
   keyboard accessibility, and any other common accessibility problems.
   ```
3. Review → Accept → Commit & Push

### 5. Continuous Validation - GitHub Actions
Three workflows run automatically on PR creation:
- **accessibility-check.yml** - axe-core testing with HTML reports
- **pa11y.yml** - WCAG2AA compliance testing  
- **ai_accessibility_check.yml** - AI-powered analysis

### 6. Delegating Future Work to Copilot Agent
1. Create a GitHub issue: "Implement keyboard-only navigation support"
2. Assign to **@github-copilot**
3. The agent creates a branch, commits fixes, and opens a PR

## What You'll Learn

You'll fix 13+ accessibility violations:
- ❌ Poor color contrast → ✅ WCAG compliant colors
- ❌ Missing alt text → ✅ Descriptive image labels  
- ❌ Wrong heading order → ✅ Proper H1→H2→H3 hierarchy
- ❌ Unlabeled forms → ✅ Accessible form controls

## Key Takeaways

| Stage | Tool | Interaction |
|-------|------|-------------|
| Manual snapshot | Accessibility Insights FastPass | Browser extension |
| Real-time hints | Axe Linter | VS Code Problems panel |
| Semi-AI fixes | Copilot completions | Inline in VS Code |
| Full AI fix | Copilot coding agent | VS Code Chat |
| Safeguards | Three GitHub Actions | PR Checks tab |

![alt text](sequence.png)

## Resources

- [Accessibility Insights](https://accessibilityinsights.io/) - Microsoft's testing tools
- [Axe Linter for VS Code](https://marketplace.visualstudio.com/items?itemName=deque-systems.vscode-axe-linter) - Automated accessibility checks

---

### How This Was Created

Generated with AI using this prompt:
```
create a simple html file to showcase how to fix accessibility issues. make the page deliberately non accessibility with a few issues. use plain html
```

**Result**: Two HTML files, 13+ accessibility patterns, automated testing workflows, and comprehensive learning guide.
