# GitHub Workflow Setup

## AI Accessibility Check Workflow

This workflow uses GitHub Models API to perform AI-powered accessibility analysis on HTML files in your repository.

### Setup Required

1. **Get a GitHub Models Token**:
   - Visit [GitHub Models Marketplace](https://github.com/marketplace/models)
   - Sign up for access to GitHub Models
   - Generate an API token

2. **Add Repository Secret**:
   - Go to your repository settings
   - Navigate to Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `MODELS_TOKEN`
   - Value: Your GitHub Models API token

3. **Verify Setup**:
   - Push changes to trigger the workflow
   - Check the Actions tab to see if the workflow runs successfully

### What the Workflow Does

- Analyzes HTML files for accessibility issues using GPT-4o
- Generates detailed reports with WCAG 2.1 AA compliance insights
- Uploads analysis results as artifacts

### Troubleshooting

If you see "Context access might be invalid: MODELS_TOKEN" warnings:
- This is a VS Code linting warning, not an actual error
- The workflow will work correctly once you add the secret
- The warnings will disappear once the secret exists in your repository
