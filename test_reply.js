const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
console.log(html.includes('reply-parent-user-login'));
