const fs = require('fs');
const js = fs.readFileSync('index.html', 'utf8');
const testMessages = js.match(/const testMessages = \[([\s\S]*?)\];/)[1];
console.log(testMessages);
