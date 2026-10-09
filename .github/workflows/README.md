# GitHub Workflow Setup

## AI Accessibility Check Workflow

This workflow uses the [GitHub Copilot SDK](https://github.com/github/copilot-sdk) (Python) to perform AI-powered accessibility analysis on HTML files in your repository.

### Setup Required

Choose **one** authentication option:

**Option A: Personal repository (recommended for forks)**

1. Create a [fine-grained personal access token](https://github.com/settings/personal-access-tokens/new) with the **Copilot Requests** permission. The account must have a GitHub Copilot subscription (the free tier works).
2. Add it as a repository secret:
   - Go to your repository settings
   - Navigate to Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `COPILOT_GITHUB_TOKEN`
   - Value: Your token

**Option B: Organization repository**

No secret is needed. Make sure the organization policy **Allow use of Copilot CLI billed to the organization** is enabled. The workflow uses the built-in `GITHUB_TOKEN` with the `copilot-requests: write` permission. See [Using Copilot CLI in GitHub Actions with GITHUB_TOKEN](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-in-actions).

**Optional:** set a `COPILOT_MODEL` repository variable (for example `gpt-5.4` or `claude-sonnet-5`) to choose the model. Otherwise the Copilot default model is used.

**Verify setup:** push changes and check the Actions tab. The analysis runs in mock mode if Copilot authentication isn't available.

### What the Workflow Does

- Analyzes HTML files for accessibility issues using GitHub Copilot
- Generates detailed reports with WCAG 2.1 AA compliance insights
- Uploads analysis results as artifacts

### Troubleshooting

If you see "Context access might be invalid: COPILOT_GITHUB_TOKEN" warnings:
- This is a VS Code linting warning, not an actual error
- The workflow will work correctly once you add the secret
- The warnings will disappear once the secret exists in your repository
