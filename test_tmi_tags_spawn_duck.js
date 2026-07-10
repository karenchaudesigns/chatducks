const fs = require('fs');
const js = fs.readFileSync('index.html', 'utf8');

// The `tags.username` in tmi.js is strictly lowercased. `tags['display-name']` has the casing.
// Let's modify `handleIncomingMessage` to pass the `display-name` or fallback to `username` to `spawnDuck`.
// And in `handleIncomingMessage`, we'll change `tags.username` to `tags['display-name'] || tags.username`.
