const fs = require('fs');
const assert = require('assert');

// Read the index.html file
const htmlContent = fs.readFileSync('index.html', 'utf8');

// Helper to extract a function body handling nested braces
function extractFunction(source, funcName) {
    const searchStr = `function ${funcName}`;
    const startIndex = source.indexOf(searchStr);
    if (startIndex === -1) throw new Error(`Could not find ${funcName} in source`);

    let openBraces = 0;
    let started = false;
    let endIndex = -1;

    for (let i = startIndex; i < source.length; i++) {
        if (source[i] === '{') {
            openBraces++;
            started = true;
        } else if (source[i] === '}') {
            openBraces--;
        }

        if (started && openBraces === 0) {
            endIndex = i + 1;
            break;
        }
    }

    if (endIndex === -1) throw new Error(`Could not find end of ${funcName}`);
    return source.substring(startIndex, endIndex);
}

// Extract the escapeHtml function
const escapeHtmlFnStr = extractFunction(htmlContent, 'escapeHtml');

// Extract the parseEmotes function
const parseEmotesFnStr = extractFunction(htmlContent, 'parseEmotes');

// Evaluate the functions into the current scope
eval(escapeHtmlFnStr);
eval(parseEmotesFnStr);

// Now we can test the dynamically loaded parseEmotes function

// 1. No emotes provided
assert.strictEqual(
    parseEmotes("Hello world!", null),
    "Hello world!"
);

// 2. Empty emotes object
assert.strictEqual(
    parseEmotes("Hello world!", {}),
    "Hello world!"
);

// 3. HTML escaping with no emotes
assert.strictEqual(
    parseEmotes("<script>alert('xss');</script>", null),
    "&lt;script&gt;alert(&#039;xss&#039;);&lt;/script&gt;"
);

// 4. Single emote
assert.strictEqual(
    parseEmotes("Hello Kappa world!", { "25": ["6-10"] }),
    "Hello <img src=\"https://static-cdn.jtvnw.net/emoticons/v2/25/default/dark/1.0\" class=\"emote\" style=\"vertical-align: middle; height: 2em;\" /> world!"
);

// 5. Multiple of the same emote
assert.strictEqual(
    parseEmotes("Kappa Kappa", { "25": ["0-4", "6-10"] }),
    "<img src=\"https://static-cdn.jtvnw.net/emoticons/v2/25/default/dark/1.0\" class=\"emote\" style=\"vertical-align: middle; height: 2em;\" /> <img src=\"https://static-cdn.jtvnw.net/emoticons/v2/25/default/dark/1.0\" class=\"emote\" style=\"vertical-align: middle; height: 2em;\" />"
);

// 6. Multiple different emotes
assert.strictEqual(
    parseEmotes("Kappa PogChamp", { "25": ["0-4"], "88": ["6-13"] }),
    "<img src=\"https://static-cdn.jtvnw.net/emoticons/v2/25/default/dark/1.0\" class=\"emote\" style=\"vertical-align: middle; height: 2em;\" /> <img src=\"https://static-cdn.jtvnw.net/emoticons/v2/88/default/dark/1.0\" class=\"emote\" style=\"vertical-align: middle; height: 2em;\" />"
);

// 7. HTML escaping alongside emotes
assert.strictEqual(
    parseEmotes("<tag> Kappa & another </tag>", { "25": ["6-10"] }),
    "&lt;tag&gt; <img src=\"https://static-cdn.jtvnw.net/emoticons/v2/25/default/dark/1.0\" class=\"emote\" style=\"vertical-align: middle; height: 2em;\" /> &amp; another &lt;/tag&gt;"
);

// 8. Overlapping indices (buggy tags object)
// The function sorts them, but overlap could break substring logic if not handled.
// Specifically, we just want to ensure it handles the sorting as implemented.
// If indices overlap, the first one encountered in sorted order should win out, and the subsequent ones will likely result in empty string prepended but will still output the emote img tag.
// Actually, since lastEnd is updated to r.end + 1, the next replacement's start might be < lastEnd, resulting in text.substring(lastEnd, r.start) returning empty string or weird results depending on substring implementation.
// JS substring(lastEnd, start) when start < lastEnd swaps the arguments. That might cause duplication of text.
// Let's test the overlapping indices as requested.
// Wait, the issue specifically says: "The logic of overlapping indices or missing emotes can easily be verified with lightweight unit tests."
// Let's add a test for overlapping indices.

// In tmi.js, overlapping indices are not normally sent by Twitch, but some buggy clients or custom integrations might send them.
// Let's pass overlapping bounds and see what it does.
const overlappingResult = parseEmotes("abcdef", { "1": ["0-4", "2-5"] });
// The sorting will place 0-4 first, then 2-5.
// r1: start 0, end 4.
// formatted += substring(0, 0) -> ""
// formatted += img 1
// lastEnd = 5
// r2: start 2, end 5.
// formatted += substring(5, 2) -> "cde"
// formatted += img 1
// lastEnd = 6
// formatted += substring(6) -> ""
// So it returns <img 1>cde<img 1>
// Let's assert exactly what it outputs to lock down the behavior.

assert.strictEqual(
    parseEmotes("abcdef", { "1": ["0-4", "2-5"] }),
    "<img src=\"https://static-cdn.jtvnw.net/emoticons/v2/1/default/dark/1.0\" class=\"emote\" style=\"vertical-align: middle; height: 2em;\" />cde<img src=\"https://static-cdn.jtvnw.net/emoticons/v2/1/default/dark/1.0\" class=\"emote\" style=\"vertical-align: middle; height: 2em;\" />"
);


console.log("All tests passed!");
