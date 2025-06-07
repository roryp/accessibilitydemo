import requests
import json
import os
import sys

def call_github_models(prompt):
    """Call GitHub Models API with GPT-4o"""
    try:
        # Check if token is available
        token = os.environ.get('MODELS_TOKEN')
        if not token:
            return "Error: MODELS_TOKEN environment variable not set. Please configure the GitHub Models API token in repository secrets."
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4.1",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert web accessibility consultant with deep knowledge of WCAG 2.1 AA guidelines, Section 508 compliance, and modern accessibility best practices. Provide detailed, actionable feedback on HTML accessibility issues."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 8000
        }
        
        response = requests.post(
            "https://models.inference.ai.azure.com/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Error calling GitHub Models: {str(e)}"

def mock_analysis(filename, html_content):
    """Mock analysis for testing when API token is not available"""
    return f"""# Mock Accessibility Analysis for {filename}

## Summary
This is a mock analysis showing what the AI would analyze. To get real AI analysis, configure the MODELS_TOKEN environment variable with your GitHub Models API token.

## What would be analyzed:
- **File size**: {len(html_content)} characters
- **HTML structure**: Would analyze semantic structure and heading hierarchy
- **Forms and inputs**: Would check for proper labels and accessibility
- **Images**: Would verify alt text and decorative vs informative usage
- **Color and contrast**: Would assess WCAG compliance
- **Keyboard navigation**: Would verify tab order and focus management
- **ARIA implementation**: Would check for proper ARIA usage

## Next steps:
1. Get a GitHub Models API token from: https://github.com/marketplace/models
2. Set the MODELS_TOKEN environment variable
3. Run the script again for full AI analysis

## Basic HTML Structure Found:
- Contains {html_content.count('<img')} image tags
- Contains {html_content.count('<input')} input elements
- Contains {html_content.count('<button')} button elements
- Contains {html_content.count('<a ')} link elements
"""

def analyze_html_file(filename):
    """Advanced AI analysis of HTML file for accessibility"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check if we have a token for real analysis
        token = os.environ.get('MODELS_TOKEN')
        if not token:
            print(f"No MODELS_TOKEN found - using mock analysis for {filename}")
            ai_response = mock_analysis(filename, html_content)
        else:
            # Enhanced prompt optimized for GPT-4o's capabilities  
            prompt = f"""Perform a comprehensive accessibility audit of this HTML code. Analyze it against WCAG 2.1 AA guidelines and provide detailed findings.

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
            
            ai_response = call_github_models(prompt)
        
        return {
            "file": filename,
            "analysis": ai_response
        }
    except Exception as e:
        return {
            "file": filename,
            "analysis": f"Error reading file: {str(e)}"
        }
  
def main():
    print("🤖 AI Accessibility Analyzer Starting...")
    print("=" * 50)
    
    # Check for token
    token = os.environ.get('MODELS_TOKEN')
    if not token:
        print("⚠️  MODELS_TOKEN not found - running in mock mode")
        print("   To get real AI analysis:")
        print("   1. Get token from: https://github.com/marketplace/models")
        print("   2. Set environment variable: MODELS_TOKEN=your_token")
        print()
    else:
        print("✅ MODELS_TOKEN found - running real AI analysis")
        print()
    
    results = []
      # Analyze HTML files
    html_files = ["accessibility-issues-demo.html", "accessibility-fixed-demo.html"]
    for filename in html_files:
        if os.path.exists(filename):
            print(f"📄 Analyzing {filename}...")
            result = analyze_html_file(filename)
            results.append(result)
            print(f"✅ Completed analysis of {filename}")
        else:
            print(f"❌ File {filename} not found, skipping...")
    
    if not results:
        print("❌ No HTML files found to analyze!")
        return
    
    # Save results
    print("\n💾 Saving results...")
    with open('ai_accessibility_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("✅ Saved results to ai_accessibility_results.json")
    
    # Create detailed markdown report
    with open('ai_accessibility_report.md', 'w', encoding='utf-8') as f:
        f.write("# AI-Powered Accessibility Analysis Report\n\n")
        if token:
            f.write("*Analysis performed by GPT-4o via GitHub Models*\n\n")
        else:
            f.write("*Mock analysis - configure MODELS_TOKEN for real AI analysis*\n\n")
        f.write("This report provides accessibility analysis based on WCAG 2.1 AA guidelines.\n\n")
        
        for result in results:
            f.write(f"## Analysis: {result['file']}\n\n")
            f.write(f"{result['analysis']}\n\n")
            f.write("---\n\n")
    
    print("✅ Saved report to ai_accessibility_report.md")
    print("\n🎉 AI accessibility analysis complete!")
    print(f"📊 Analyzed {len(results)} files")
    print("📄 Check ai_accessibility_report.md for detailed results")

if __name__ == "__main__":
    main()
