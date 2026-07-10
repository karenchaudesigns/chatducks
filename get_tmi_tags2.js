const fs = require('fs');
const js = fs.readFileSync('index.html', 'utf8');
const handleIncomingMessage = js.match(/function handleIncomingMessage\(([^)]+)\) {([\s\S]*?)}/)[0];
console.log(handleIncomingMessage);
