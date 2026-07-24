const fs = require('fs');
const assert = require('assert');

// Read the index.html file
const html = fs.readFileSync('index.html', 'utf8');

// Extract the generateColorFromUsername function using a more robust regular expression
const match = html.match(/function\s+generateColorFromUsername\s*\([^\)]*\)\s*\{[\s\S]*?return\s+.*?;[\s\n]*\}/);

if (!match) {
    console.error("Could not find generateColorFromUsername in index.html");
    process.exit(1);
}

// Evaluate the function in the current scope
eval(match[0]);

try {
    // 1. Same input produces same output
    assert.strictEqual(generateColorFromUsername('jules'), generateColorFromUsername('jules'), 'Same input should produce same output');

    // 2. Format is correct
    const result = generateColorFromUsername('testuser');
    assert.match(result, /^hsl\(\d+, 85%, 60%\)$/, 'Format should be hsl(X, 85%, 60%)');

    // 3. Hue is bounded within 0-359
    const testStrings = ['a', 'ab', 'abc', 'abcd', 'abcde', 'test_user_123', '', 'really_long_username_that_might_cause_large_hash'];
    for (const str of testStrings) {
        const res = generateColorFromUsername(str);
        const resMatch = res.match(/^hsl\((\d+), 85%, 60%\)$/);
        assert.ok(resMatch, `Invalid format for string "${str}": ${res}`);
        const hue = parseInt(resMatch[1], 10);
        assert.ok(hue >= 0 && hue < 360, `Hue should be between 0 and 359, got ${hue}`);
    }

    // 4. Check a known hash value to prevent regressions in the hash logic
    assert.strictEqual(generateColorFromUsername('test'), 'hsl(58, 85%, 60%)');

    // 5. Test different usernames to ensure different hues are generated (for some known inputs)
    assert.notStrictEqual(generateColorFromUsername('user1'), generateColorFromUsername('user2'));

    console.log('All tests passed for generateColorFromUsername!');
} catch (error) {
    console.error('Test failed:', error);
    process.exit(1);
}
