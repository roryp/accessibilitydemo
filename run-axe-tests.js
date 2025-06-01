const puppeteer = require('puppeteer');
const { AxePuppeteer } = require('@axe-core/puppeteer');
const fs = require('fs');

async function runAxe(url, outputFile) {
  console.log(`Testing ${url} for accessibility issues...`);
  
  try {
    // Launch a headless browser
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    // Navigate to the URL
    await page.goto(url, { waitUntil: 'networkidle2' });
    
    // Run axe on the page
    const results = await new AxePuppeteer(page).analyze();
    
    // Save results to file
    fs.writeFileSync(outputFile, JSON.stringify(results, null, 2));
    
    console.log(`✅ Test completed. Results saved to ${outputFile}`);
    console.log(`Found ${results.violations.length} accessibility violations.`);
    
    // Close the browser
    await browser.close();
    
    return results;
  } catch (error) {
    console.error('Error running accessibility tests:', error);
    // Create an empty structure if there's an error
    fs.writeFileSync(outputFile, JSON.stringify({
      violations: [],
      incomplete: [],
      passes: []
    }, null, 2));
    console.log(`❌ Test failed. Empty results file created at ${outputFile}`);
  }
}

// Run tests on both files
async function main() {
  await runAxe('http://localhost:3000/accessibility-issues-demo.html', 'accessibility-issues-results.json');
  await runAxe('http://localhost:3000/accessibility-fixed-demo.html', 'accessibility-fixed-results.json');
}

main().catch(console.error);
