# Accessibility Demo  IDE & Browser-Only Walk-through

Move the **[accessibilitydemo](https://github.com/roryp/accessibilitydemo)** repository from failing WCAG checks to full compliance without touching a terminaleverything happens in your **browser** or **VS Code**.

> **Flow:** Manual discovery -> Semi-AI fixes -> Full-AI agent -> CI validation

---

## 1  Setup (UI only)

1. **Fork** the repository on GitHub.  
2. In VS Code choose **File -> Clone Repository** and paste the URL of **your fork**.  
3. Open the workspace and choose **Trust** when prompted.

All subsequent Git operations (commit, push, pullrequest) happen through the **Source Control** panel or the **GitHub website**no CLI required.

---

## 2  Initial Testing  Accessibility Insights & Axe linter

1. Serve or open **`index.html`** in Chrome/Edge.  
2. Click the **Accessibility Insights for Web** extension icon.  
3. Run a **FastPass** to capture an automated + tabstops report. (Export if you like.)  
4. Optional but handy: In VS Code run **Axe linter** extension. This shows identical issues in the **Problems** panel.  
5. Fix any lowhanging fruit right away, then rerun FastPass to confirm they are gone.

Why both? Axe linter gives realtime feedback while you edit; FastPass provides a formal report you can export or attach to a PR.

---

## 3  Semi AI Fixes with Copilot Completions (IDE)

1. Open a file flagged by FastPass/Axelinter.  
2. Add a guiding comment such as `<!-- TODO add alt text -->` and press **Tab** to accept Copilots suggestion.  
3. Stage the change (Source Control "+" icon) and commit.  
4. Repeat for a handful of issues so Copilot learns the pattern.

---

## 4  Full AI Fixes with Copilot Agent (IDE)

1. Open **Copilot Chat** (Option+Command+I or via the sidebar icon).  
2. Prompt:

   ```
   Resolve every remaining WCAG 2.2 AA violation across the workspace. Keep visual design unchanged.
   ```

3. Review the multifile diff Copilot proposes.  
4. Click **Accept**, then **Commit** and **Push** via the Source Control panel.

---

## 5  Continuous Validation  Three GitHub Actions

Your fork already contains three purposebuilt workflows in **`.github/workflows/`**:

| Workflow file | Job name | What it does |
|---------------|----------|--------------|
| `accessibility-check.yml` | Accessibility Check | Launches a local server, runs `run-axe-tests.js` (axe-core) on the demo pages, generates an HTML report, and fails if the fixed page still shows violations. |
| `pa11y.yml` | Pa11y Accessibility Tests | Executes `pa11y-ci` (axe runner) against the pages in headless Chrome and uploads the CLI logs as artifacts. |
| `ai_accessibility_check.yml` | AI Accessibility Check | Runs `ai_accessibility_analyzer.py`; if a `MODELS_TOKEN` secret is present it queries GitHub Models for deeper AI insights, otherwise performs mock analysis. Outputs JSON and Markdown artifacts. |

### How these integrate with your testing loop

1. After you Publish Branch & Create PR from VS Code, open the pull request in the browser.  
2. Watch the Checks tabeach workflow reports status.  
3. If any step fails, click its name -> Artifacts to download the detailed report.  
4. Go back to VS Code, fix code with Copilot completions/agent, commit & push. Checks automatically rerun.  
5. Merge when all three checks are green.

<details>
<summary>Badge snippet (add to README.md)</summary>

```markdown
![Accessibility Check](https://github.com/<your-user>/accessibilitydemo/actions/workflows/accessibility-check.yml/badge.svg)
![Pa11y](https://github.com/<your-user>/accessibilitydemo/actions/workflows/pa11y.yml/badge.svg)
![AI A11y](https://github.com/<your-user>/accessibilitydemo/actions/workflows/ai_accessibility_check.yml/badge.svg)
```
</details>

---

## 6  Delegating Future Work to Copilot Agent (Browser)

1. In GitHub open Issues -> New issue.  
2. Title: "Implement keyboard-only navigation support".  
3. Body: "Ensure full operability without a pointing device per WCAG 2.2."  
4. Assign the issue to **@github-copilot**.

The coding agent will:

* Create a branch.  
* Commit fixes.  
* Open a PR referencing CI evidence.

Review, merge, done.

---

## 7  Key Takeaways

| Stage | Tool | Interaction |
|-------|------|-------------|
| Manual snapshot | Accessibility Insights FastPass | Browser extension |
| Realtime hints | Axe linter | VS Code Problems panel |
| Semi AI fixes | Copilot completions | Inline in VS Code |
| Full AI fix | Copilot coding agent | VS Code Chat |
| Safeguards | Three GitHub Actions | PR Checks tab |

With just **IDE + browser**, you can discover, remediate, verify, and enforce accessibility complianceall tracked in Git.

---

### References

* Accessibility Insights for Web: <https://accessibilityinsights.io/docs/en/web/overview/>  
* Axelinter for VS Code: <https://marketplace.visualstudio.com/items?itemName=deque-systems.vscode-axe-linter>  
* GitHub Copilot & Agents: <https://docs.github.com/en/copilot>  
* Pa11y CI: <https://github.com/pa11y/pa11y-ci>  
* WCAG 2.2 Quick Ref: <https://www.w3.org/WAI/WCAG22/quickref/>