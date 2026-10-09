"""AI accessibility analyzer powered by the GitHub Copilot SDK.

Authentication (first match wins, handled by the Copilot runtime):
  - COPILOT_GITHUB_TOKEN / GH_TOKEN / GITHUB_TOKEN environment variables
  - Stored Copilot CLI or GitHub CLI (`gh auth login`) credentials

Optional: set COPILOT_MODEL to choose a model (defaults to the runtime default).
Falls back to a mock analysis when no Copilot authentication is available.
"""

import asyncio
import json
import os
import sys

from copilot import CopilotClient

# Allow emoji output on consoles with legacy encodings (e.g. Windows cp1252).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HTML_FILES = ["accessibility-issues-demo.html", "accessibility-fixed-demo.html"]
RESPONSE_TIMEOUT_SECONDS = 600

SYSTEM_PROMPT = (
    "You are an expert web accessibility consultant with deep knowledge of WCAG 2.1 AA "
    "guidelines, Section 508 compliance, and modern accessibility best practices. Provide "
    "detailed, actionable feedback on HTML accessibility issues."
)


def build_prompt(html_content):
    return f"""Perform a comprehensive accessibility audit of this HTML code. Analyze it against WCAG 2.1 AA guidelines and provide detailed findings.

Focus on these critical areas:
1. Semantic HTML Structure: Proper heading hierarchy, landmark elements, semantic tags
2. Images & Media: Alt text quality, decorative vs informative images, complex images
3. Forms & Interactive Elements: Labels, fieldsets, error handling, focus management
4. Keyboard Navigation: Tab order, focus indicators, keyboard traps, skip links
5. Color & Contrast: Text contrast ratios, color-only information conveyance
6. ARIA Implementation: Proper ARIA attributes, roles, states, and properties
7. Document Structure: Language attributes, page titles, meta information
8. Dynamic Content: Live regions, status updates, progressive enhancement

For each issue found, provide:
- Severity: Critical/High/Medium/Low
- WCAG Guideline: Specific guideline reference
- Issue Description: Clear explanation of the problem
- Code Location: Specific HTML elements affected
- Remediation: Exact code fixes with before/after examples
- User Impact: How this affects users with disabilities

HTML Code to Analyze:
{html_content}

Provide your analysis in a structured format with clear sections and actionable recommendations."""


def mock_analysis(filename, html_content, reason):
    """Mock analysis used when Copilot is not available"""
    return f"""# Mock Accessibility Analysis for {filename}

## Summary
This is a mock analysis showing what the AI would analyze. Reason: {reason}

## What would be analyzed:
- **File size**: {len(html_content)} characters
- **HTML structure**: Would analyze semantic structure and heading hierarchy
- **Forms and inputs**: Would check for proper labels and accessibility
- **Images**: Would verify alt text and decorative vs informative usage
- **Color and contrast**: Would assess WCAG compliance
- **Keyboard navigation**: Would verify tab order and focus management
- **ARIA implementation**: Would check for proper ARIA usage

## Next steps:
1. Locally: sign in with `gh auth login` (account with a GitHub Copilot subscription)
2. In GitHub Actions: add a `COPILOT_GITHUB_TOKEN` repository secret (fine-grained PAT with the "Copilot Requests" permission)
3. Run the script again for full AI analysis

## Basic HTML Structure Found:
- Contains {html_content.count('<img')} image tags
- Contains {html_content.count('<input')} input elements
- Contains {html_content.count('<button')} button elements
- Contains {html_content.count('<a ')} link elements
"""


async def analyze_with_copilot(client, model, html_content):
    async with await client.create_session(
        model=model,
        system_message={"mode": "replace", "content": SYSTEM_PROMPT},
        # Pure text analysis: the HTML is inlined in the prompt, so no tools are needed.
        available_tools=[],
    ) as session:
        event = await session.send_and_wait(
            build_prompt(html_content), timeout=RESPONSE_TIMEOUT_SECONDS
        )
        if event is None or not getattr(event.data, "content", None):
            return "Error: Copilot returned no response."
        return event.data.content


async def analyze_html_file(client, model, filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        return {"file": filename, "analysis": f"Error reading file: {e}"}

    if client is None:
        print(f"No Copilot authentication - using mock analysis for {filename}")
        analysis = mock_analysis(filename, html_content, "GitHub Copilot authentication not available.")
    else:
        try:
            analysis = await analyze_with_copilot(client, model, html_content)
        except Exception as e:
            analysis = f"Error calling GitHub Copilot SDK: {e}"
    print(f"✅ Completed analysis of {filename}")
    return {"file": filename, "analysis": analysis}


async def start_client():
    """Start the Copilot client; return None if it can't start or isn't authenticated."""
    client = CopilotClient()
    try:
        await client.start()
        status = await client.get_auth_status()
        if status.isAuthenticated:
            print(f"✅ Authenticated with GitHub Copilot ({status.statusMessage}) - running real AI analysis")
            return client
        print(f"⚠️  Not authenticated with GitHub Copilot: {status.statusMessage}")
    except Exception as e:
        print(f"⚠️  Could not start GitHub Copilot SDK: {e}")
    try:
        await client.stop()
    except Exception:
        pass
    return None


def write_reports(results, used_ai, model):
    print("\n💾 Saving results...")
    with open("ai_accessibility_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("✅ Saved results to ai_accessibility_results.json")

    with open("ai_accessibility_report.md", "w", encoding="utf-8") as f:
        f.write("# AI-Powered Accessibility Analysis Report\n\n")
        if used_ai:
            f.write(f"*Analysis performed via the GitHub Copilot SDK (model: {model or 'default'})*\n\n")
        else:
            f.write("*Mock analysis - authenticate with GitHub Copilot for real AI analysis*\n\n")
        f.write("This report provides accessibility analysis based on WCAG 2.1 AA guidelines.\n\n")
        for result in results:
            f.write(f"## Analysis: {result['file']}\n\n")
            f.write(f"{result['analysis']}\n\n")
            f.write("---\n\n")
    print("✅ Saved report to ai_accessibility_report.md")


async def main():
    print("🤖 AI Accessibility Analyzer Starting (GitHub Copilot SDK)...")
    print("=" * 50)

    files = [name for name in HTML_FILES if os.path.exists(name)]
    for name in set(HTML_FILES) - set(files):
        print(f"❌ File {name} not found, skipping...")
    if not files:
        print("❌ No HTML files found to analyze!")
        return

    model = os.environ.get("COPILOT_MODEL") or None
    client = await start_client()
    if client is None:
        print("   To get real AI analysis:")
        print("   - Locally: run `gh auth login` with a Copilot-enabled account")
        print("   - In CI: set the COPILOT_GITHUB_TOKEN secret")
        print()

    try:
        for name in files:
            print(f"📄 Analyzing {name}...")
        results = await asyncio.gather(*(analyze_html_file(client, model, name) for name in files))
    finally:
        if client is not None:
            await client.stop()

    write_reports(results, client is not None, model)
    print("\n🎉 AI accessibility analysis complete!")
    print(f"📊 Analyzed {len(results)} files")
    print("📄 Check ai_accessibility_report.md for detailed results")


if __name__ == "__main__":
    asyncio.run(main())
