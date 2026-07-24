const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const fnMatch = html.match(/function\s+generateColorFromUsername\s*\([^\)]*\)\s*\{([\s\S]*?return\s+.*?;)\s*\}/);

if(fnMatch) {
    console.log("Matched!");
} else {
    console.log("Not matched");
}
