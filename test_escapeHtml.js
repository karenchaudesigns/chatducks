const assert = require('assert');
const fs = require('fs');

// Extract the function from index.html
const html = fs.readFileSync('index.html', 'utf8');

// Use a regular expression to find the escapeHtml function
// It looks for: function escapeHtml(unsafe) { ... }
const match = html.match(/function escapeHtml\(unsafe\) \{([\s\S]*?)\n\s*\}/);

if (!match) {
    console.error("Could not find escapeHtml function in index.html");
    process.exit(1);
}

// Create the function using the extracted body
const escapeHtml = new Function('unsafe', match[1]);

console.log("Running tests for escapeHtml...");

let passed = 0;
let failed = 0;

function runTest(name, input, expected) {
    try {
        const result = escapeHtml(input);
        assert.strictEqual(result, expected);
        console.log(`✅ PASS: ${name}`);
        passed++;
    } catch (e) {
        console.error(`❌ FAIL: ${name}`);
        console.error(`   Expected: '${expected}'`);
        console.error(`   Got:      '${escapeHtml(input)}'`);
        failed++;
    }
}

// 1. Happy path: plain text
runTest('Plain text without special characters', 'hello world', 'hello world');

// 2. Edge case: empty string
runTest('Empty string', '', '');

// 3. Characters to escape (individual)
runTest('Escape ampersand', '&', '&amp;');
runTest('Escape less than', '<', '&lt;');
runTest('Escape greater than', '>', '&gt;');
runTest('Escape double quote', '"', '&quot;');
runTest('Escape single quote', "'", '&#039;');

// 4. Multiple occurrences of the same character
runTest('Multiple ampersands', '&&&', '&amp;&amp;&amp;');
runTest('Multiple mixed characters', '<>""\'\'', '&lt;&gt;&quot;&quot;&#039;&#039;');

// 5. Complex string
runTest(
    'Complex XSS-like string',
    '<script>alert("XSS & \'hacked\'")</script>',
    '&lt;script&gt;alert(&quot;XSS &amp; &#039;hacked&#039;&quot;)&lt;/script&gt;'
);

// 6. Realistic chat message
runTest(
    'Realistic chat message',
    'I love this stream <3 It\'s the "best" & the funniest!',
    'I love this stream &lt;3 It&#039;s the &quot;best&quot; &amp; the funniest!'
);

console.log(`\nTest Summary: ${passed} passed, ${failed} failed`);

if (failed > 0) {
    process.exit(1);
}
