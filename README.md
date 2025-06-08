# Accessibility Issues Demo - Learning Guide 

![image](image.png)
This project demonstrates common web accessibility issues and their solutions through two HTML files: one with deliberate accessibility problems and another showing how to fix them. Perfect for developers learning accessibility best practices.

## 🚀 Quick Start

1. **Explore the demos**: Open both HTML files in your browser
   - `accessibility-issues-demo.html` - Shows common accessibility violations
   - `accessibility-fixed-demo.html` - Shows proper accessibility implementation
2. **Compare the differences**: Use keyboard navigation and screen readers on both
3. **Run accessibility tests**: Use automated tools to see the violations
4. **Learn from the patterns**: Review this guide to understand each issue and fix

## What You'll Learn

This project covers **13+ common accessibility issues** that developers encounter:

### Core Issues Demonstrated

1. **Poor Color Contrast** - Yellow text on white backgrounds that fail WCAG standards
2. **Missing Alt Text** - Images without proper alternative text descriptions
3. **Improper Heading Hierarchy** - Skipping heading levels (h3 before h1)
4. **Forms Without Labels** - Input fields missing proper labels and instructions
5. **Non-Semantic Elements** - Using divs instead of proper buttons and links
6. **Poor Link Text** - "Click here" links that lack context
7. **Data Tables Without Headers** - Tables missing proper th elements and scope
8. **Blinking/Flashing Content** - Auto-animations that can trigger seizures
9. **Text Too Small** - Font sizes below 16px that are hard to read
10. **Missing Language Declaration** - No lang attribute on HTML element
11. **Auto-playing Media** - Videos that auto-play without user control
12. **Inaccessible Custom Controls** - Dropdowns without keyboard support
13. **Poor Focus Management** - Elements without visible focus indicators

### Best Practices You'll Master

- **Semantic HTML Structure** with proper landmarks
- **ARIA Implementation** for complex interactive elements
- **Keyboard Accessibility** patterns and focus management
- **Screen Reader Support** with descriptive content
- **Color and Contrast** meeting WCAG AA standards
- **Responsive Design** with touch-friendly targets

## 🧪 Testing Your Accessibility

### Manual Testing
1. **Keyboard Navigation**: Tab through both demos - notice the differences
2. **Screen Reader**: Use NVDA, JAWS, or VoiceOver to hear how they sound
3. **Visual Inspection**: Check color contrast and text sizing
4. **Browser Tools**: Use Chrome DevTools Lighthouse accessibility audit

### Automated Testing Tools
- **Accessibility Insights** - Microsoft's free browser extension ([Download](https://accessibilityinsights.io/downloads))
- **axe DevTools** - Browser extension for automated accessibility testing
- **WAVE** - Web accessibility evaluation tool
- **Lighthouse** - Built into Chrome DevTools

### 📊 Continuous Integration Testing

This project includes **three automated testing workflows** that run on every push and pull request:

#### GitHub Actions Workflow (axe-core)
**Location:** `.github/workflows/accessibility-check.yml`

- Tests both HTML files with axe-core engine
- Generates detailed HTML reports with violation descriptions
- Uploads results as downloadable artifacts
- Comments on pull requests with findings
- Fails builds if fixed demo has serious violations

#### Pa11y Command-Line Testing  
**Location:** `.github/workflows/pa11y.yml`

- Industry-standard command-line accessibility testing
- Tests against WCAG2AA standards with concurrent execution
- Provides CLI-focused reports ideal for developers
- Automatically comments on pull requests with collapsible results

#### 🤖 AI-Powered Accessibility Analysis
**Location:** `.github/workflows/ai_accessibility_check.yml`

📊 **[View Detailed Sequence Diagram](sequence_diagram.md)** - Complete workflow visualization created with PlantUML

- **Advanced AI Analysis**: Uses GPT-4.1 via GitHub Models for comprehensive accessibility analysis
- **Expert-Level Insights**: Provides detailed, human-readable analysis and actionable recommendations
- **WCAG 2.1 AA Compliance**: Analyzes semantic HTML, ARIA implementation, keyboard navigation, and more
- **Automated Reporting**: Generates both JSON data and detailed markdown reports

**What it analyzes:**
- Semantic HTML structure and heading hierarchy  
- Images and media accessibility (alt text quality)
- Forms and interactive elements
- Keyboard navigation patterns
- Color and contrast compliance
- ARIA implementation
- Document structure and language attributes

**Setup Required:**
1. Get a GitHub personal access token with Models scope
2. Add it as repository secret named `MODELS_TOKEN`
3. See setup instructions below for details

#### Running Tests Locally

**axe-core testing:**
```bash
npm install --save-dev @axe-core/cli puppeteer serve
npx serve . -l 3000 &
npx axe http://localhost:3000/accessibility-issues-demo.html --reporter json
```

**Pa11y testing:**
```bash
npm install -g pa11y-ci
python -m http.server 8080
pa11y http://localhost:8080/accessibility-issues-demo.html --standard WCAG2AA --runner axe
```

**AI accessibility testing:**
```bash
# Install Python dependencies
pip install requests

# Set your GitHub Models token
export MODELS_TOKEN=your_github_models_token

# Run the AI analyzer
python ai_accessibility_analyzer.py
```

```

## 📋 WCAG 2.1 Compliance Reference

- **Level A**: Minimum accessibility (basic compliance)
- **Level AA**: Standard level - **recommended for most websites**
- **Level AAA**: Highest level (required for government/critical services)

Most organizations target **WCAG 2.1 AA compliance** for the best balance of accessibility and practicality.

## 🛠️ Fixing Issues with AI Assistance

### Using GitHub Copilot for Accessibility

GitHub Copilot can help you systematically identify and fix accessibility issues. Here are effective approaches:

#### Quick Fix Prompts
```
Fix all color contrast issues in this HTML file to meet WCAG AA standards.
Add missing alt text to all images and use empty alt for decorative images.
Correct the heading hierarchy so it starts with <h1> and follows logical order.
Make all form fields properly labeled and ensure semantic button elements.
```

#### Working with GitHub Issues
Use [GitHub Copilot's coding agent](https://docs.github.com/en/copilot/using-github-copilot/coding-agent/using-copilot-to-work-on-an-issue) to systematically track and fix accessibility problems:

```bash
# Create accessibility issues
@github Create an issue for missing alt text on images in accessibility-issues-demo.html

# Start working on issues  
@github Start working on issue #123 about missing alt text

# Request comprehensive fixes
@github Fix the color contrast issues in this file to meet WCAG 2.1 AA standards
```

#### Best Practices for AI-Assisted Accessibility
- Be specific about WCAG guidelines ("fix to meet WCAG 2.1 AA")
- Ask for explanations along with fixes to learn the patterns
- Always test AI-generated solutions with accessibility tools
- Use issue templates for common accessibility patterns
- Request explanations to understand why changes improve accessibility

## 🚀 Extending This Project

### Additional Features You Could Add
- ARIA live regions with dynamic content updates
- Keyboard navigation with focus trapping for modals
- Accessible data visualizations and charts
- Mobile accessibility with touch targets and gestures
- Multi-language support with proper lang attributes

### Advanced Learning Path
1. **Start here** - Master the basic issues in this demo
2. **Practice** - Apply fixes to your own projects
3. **Automate** - Set up accessibility testing in your CI/CD pipeline
4. **Advanced patterns** - Study complex ARIA widgets and interactions
5. **Contribute** - Help improve accessibility in open source projects

## 📚 Resources for Continued Learning

- [Web Content Accessibility Guidelines (WCAG) 2.1](https://www.w3.org/WAI/WCAG21/quickref/) - Official standards
- [WebAIM](https://webaim.org/) - Practical accessibility resources and testing tools
- [A11y Project](https://www.a11yproject.com/) - Community-driven accessibility checklist
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility) - Technical implementation guides

## 🤖 How This Project Was Created

This comprehensive accessibility demo was generated using AI with this simple prompt:

```
create a simple html file to showcase how to fix accessibility issues. make the page deliberately non accessibility with a few issues. use plain html
```

**What AI Generated:**
- Two complete HTML files (broken and fixed versions)
- 13+ realistic accessibility violations and their solutions  
- Comprehensive documentation with WCAG mapping
- Three automated testing workflows (axe-core, Pa11y, and AI-powered analysis)
- Learning guidance and best practices

**Why It Worked:** The prompt was specific about the educational goal, requested both problems and solutions, and specified the technology constraint (plain HTML).

### Alternative Prompts for Similar Projects
```
Create an accessibility audit training kit with before/after HTML examples
Build a WCAG compliance demo with real-world accessibility violations  
Generate a complete accessibility testing playground for developers
```

---

**Remember:** Accessibility benefits everyone, not just users with disabilities. It improves SEO, usability, mobile experience, and creates a better web for all users.

## 🤖 AI-Powered Accessibility Analysis Setup

This project includes an advanced AI accessibility checker powered by **GPT-4.1 via GitHub Models**. The AI performs comprehensive accessibility audits that go beyond traditional automated tools.

### Setup Instructions

#### 1. Get GitHub Models Access
GitHub Models provides access to advanced AI models including GPT-4.1:
- Visit [GitHub Models](https://github.com/marketplace/models)
- Sign in with your GitHub account
- Test models directly in the interface

#### 2. Configure Repository Secrets
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

#### 3. Run the Analysis
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

---
