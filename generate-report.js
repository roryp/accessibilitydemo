const fs = require('fs');

// Read test results
const issuesResults = JSON.parse(fs.readFileSync('accessibility-issues-results.json', 'utf8'));
const fixedResults = JSON.parse(fs.readFileSync('accessibility-fixed-results.json', 'utf8'));

// Generate HTML for violations
function generateViolationHtml(violation) {
  const nodes = violation.nodes.map(node => {
    return `
      <div class="violation-node">
        <h4>HTML Element:</h4>
        <pre class="code">${escapeHtml(node.html)}</pre>
        ${node.failureSummary ? `<p class="failure-summary">${escapeHtml(node.failureSummary)}</p>` : ''}
      </div>
    `;
  }).join('');

  return `
    <div class="violation">
      <h3>${escapeHtml(violation.id)}: ${escapeHtml(violation.help)}</h3>
      <p><strong>Impact:</strong> ${violation.impact}</p>
      <p><strong>Description:</strong> ${escapeHtml(violation.description)}</p>
      <p><strong>Help:</strong> ${escapeHtml(violation.help)}</p>
      <p><a href="${violation.helpUrl}" target="_blank">Learn more</a></p>
      <div class="nodes">
        <h4>Affected Elements (${violation.nodes.length}):</h4>
        ${nodes}
      </div>
    </div>
  `;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
  if (!text) return '';
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Generate the report HTML
const report = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Accessibility Test Report</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      line-height: 1.6;
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
      color: #333;
    }
    h1, h2 {
      border-bottom: 2px solid #eaecef;
      padding-bottom: 10px;
    }
    .report-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .summary-box {
      background-color: #f6f8fa;
      border: 1px solid #ddd;
      border-radius: 5px;
      padding: 15px;
      margin-bottom: 20px;
    }
    .passing {
      color: #28a745;
    }
    .failing {
      color: #dc3545;
    }
    .violations {
      margin-top: 30px;
    }
    .violation {
      background-color: #fff;
      border: 1px solid #e1e4e8;
      border-radius: 6px;
      padding: 16px;
      margin-bottom: 16px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .violation h3 {
      margin-top: 0;
      border-bottom: 1px solid #eaecef;
      padding-bottom: 8px;
    }
    .violation-node {
      background-color: #f6f8fa;
      padding: 12px;
      border-radius: 6px;
      margin-bottom: 12px;
    }
    .code {
      background-color: #f6f8fa;
      border-radius: 3px;
      padding: 10px;
      overflow-x: auto;
      font-family: SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace;
      font-size: 85%;
    }
    .failure-summary {
      background-color: #ffe8e8;
      border-left: 3px solid #dc3545;
      padding: 8px 15px;
    }
    .tabs {
      display: flex;
      margin-bottom: 20px;
      border-bottom: 1px solid #e1e4e8;
    }
    .tab {
      padding: 10px 20px;
      cursor: pointer;
      border: 1px solid transparent;
      border-bottom: none;
      margin-bottom: -1px;
      background-color: transparent;
    }
    .tab.active {
      border-color: #e1e4e8;
      border-bottom-color: white;
      background-color: white;
      font-weight: bold;
    }
    .tab-content {
      display: none;
    }
    .tab-content.active {
      display: block;
    }
    @media (max-width: 768px) {
      .report-header {
        flex-direction: column;
      }
    }
  </style>
</head>
<body>
  <div class="report-header">
    <h1>Accessibility Test Report</h1>
    <p><strong>Date:</strong> ${new Date().toLocaleDateString()}</p>
  </div>

  <div class="tabs">
    <button class="tab active" onclick="openTab(event, 'issues')">Issues Demo</button>
    <button class="tab" onclick="openTab(event, 'fixed')">Fixed Demo</button>
  </div>

  <div id="issues" class="tab-content active">
    <h2>Issues Demo Page</h2>
    
    <div class="summary-box">
      <h3>Summary</h3>
      <p><strong>Violations:</strong> <span class="${issuesResults.violations.length > 0 ? 'failing' : 'passing'}">${issuesResults.violations.length}</span></p>
      <p><strong>Passes:</strong> ${issuesResults.passes ? issuesResults.passes.length : 0}</p>
      <p><strong>Incomplete:</strong> ${issuesResults.incomplete ? issuesResults.incomplete.length : 0}</p>
    </div>

    ${issuesResults.violations.length > 0 ? `
      <div class="violations">
        <h3>Violations (${issuesResults.violations.length})</h3>
        ${issuesResults.violations.map(violation => generateViolationHtml(violation)).join('')}
      </div>
    ` : '<p class="passing">No accessibility violations found! 🎉</p>'}
  </div>

  <div id="fixed" class="tab-content">
    <h2>Fixed Demo Page</h2>
    
    <div class="summary-box">
      <h3>Summary</h3>
      <p><strong>Violations:</strong> <span class="${fixedResults.violations.length > 0 ? 'failing' : 'passing'}">${fixedResults.violations.length}</span></p>
      <p><strong>Passes:</strong> ${fixedResults.passes ? fixedResults.passes.length : 0}</p>
      <p><strong>Incomplete:</strong> ${fixedResults.incomplete ? fixedResults.incomplete.length : 0}</p>
    </div>

    ${fixedResults.violations.length > 0 ? `
      <div class="violations">
        <h3>Violations (${fixedResults.violations.length})</h3>
        ${fixedResults.violations.map(violation => generateViolationHtml(violation)).join('')}
      </div>
    ` : '<p class="passing">No accessibility violations found! 🎉</p>'}
  </div>

  <script>
    function openTab(evt, tabName) {
      const tabContents = document.getElementsByClassName("tab-content");
      for (const tabContent of tabContents) {
        tabContent.className = tabContent.className.replace(" active", "");
      }

      const tabs = document.getElementsByClassName("tab");
      for (const tab of tabs) {
        tab.className = tab.className.replace(" active", "");
      }

      document.getElementById(tabName).className += " active";
      evt.currentTarget.className += " active";
    }
  </script>
</body>
</html>`;

// Write the report to a file
fs.writeFileSync('accessibility-report.html', report);
console.log('✅ HTML report generated at accessibility-report.html');
