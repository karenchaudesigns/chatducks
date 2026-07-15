import re

with open('index.html', 'r') as f:
    content = f.read()

# I mistakenly inserted the explicit commands BEFORE `let user = activeUsers.get(username);`
# It's accessing `user` before initialization. Let's fix that.

# Remove from current location
content = re.sub(
    r'\n            if \(\[\'!back\', \'!unlurk\', \'!bellyflop\', \'!makeadramaticentrance\'\]\.includes\(textTrim\)\) \{\n                if \(user\) \{\n                    user\.isLurking = false;\n                    user\.element\.classList\.remove\("lurking"\);\n                    user\.element\.querySelector\(\'\.duck-svg\'\)\.innerHTML = `<img src="assets/custom_ducks/\$\{username\}\.png" alt="\$\{username\}" style="width: 100%; height: 100%; object-fit: contain;" onerror="this\.onerror = \(\) => \{ this\.onerror = null; this\.parentElement\.innerHTML = getDuckSVG\(\'\$\{user\.duckColor\}\'\); \}; this\.src = \'assets/custom_ducks/\' \+ \'\$\{username\}\'\.toLowerCase\(\) \+ \'\.png\';" />`;\n                    scatterDucks\(\);\n                \}\n                return;\n            \}\n',
    '',
    content
)

# And place it AFTER `let user = activeUsers.get(username);` but before spawning new duck
unlurk_commands = r"""
            if (['!back', '!unlurk', '!bellyflop', '!makeadramaticentrance'].includes(textTrim)) {
                if (user) {
                    user.isLurking = false;
                    user.element.classList.remove("lurking");
                    user.element.querySelector('.duck-svg').innerHTML = `<img src="assets/custom_ducks/${username}.png" alt="${username}" style="width: 100%; height: 100%; object-fit: contain;" onerror="this.onerror = () => { this.onerror = null; this.parentElement.innerHTML = getDuckSVG('${user.duckColor}'); }; this.src = 'assets/custom_ducks/' + '${username}'.toLowerCase() + '.png';" />`;
                    scatterDucks();
                }
                return;
            }
"""

content = re.sub(
    r'(let user = activeUsers\.get\(username\);)',
    r'\1' + unlurk_commands,
    content
)

with open('index.html', 'w') as f:
    f.write(content)
