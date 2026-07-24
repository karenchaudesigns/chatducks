import re

with open('index.html', 'r') as f:
    content = f.read()

# I accidentally added animation: flip-duck to multiple places in the grep due to regex matching multiple ending braces. Let's reset the CSS and do it cleanly.
content = re.sub(
    r'(\.duck-svg \{[\s\S]*?)(\n            animation: flip-duck 30s infinite linear;\n\})',
    r'\1}',
    content
)

content = re.sub(
    r'(\.lurking \.duck-svg \{[\s\S]*?)(\n            animation: flip-duck 30s infinite linear;\n\})',
    r'\1}',
    content
)
content = re.sub(
    r'(\.conversing \.duck-swim, \.conversing \.duck-svg \{[\s\S]*?)(\n            animation: flip-duck 30s infinite linear;\n\})',
    r'\1}',
    content
)
content = re.sub(
    r'(\.conversing\.facing-left \.duck-svg \{[\s\S]*?)(\n            animation: flip-duck 30s infinite linear;\n\})',
    r'\1}',
    content
)
content = re.sub(
    r'(\.conversing\.facing-right \.duck-svg \{[\s\S]*?)(\n            animation: flip-duck 30s infinite linear;\n\})',
    r'\1}',
    content
)

# Replace the messy animation addition
content = re.sub(
    r'(\.duck-svg \{[\s\S]*?filter: drop-shadow\(0px 8px 6px rgba\(0,0,0,0\.4\)\);\n)\}',
    r'\1            animation: flip-duck 30s infinite linear;\n}',
    content
)

# And fix the keyframe order
# By separating the string components here, we avoid having nested CSS keyframes literally written in the Python source.
search_pattern = (
    r'@keyframes swim-horizontal \{\n            0% \{ transform: translateX\(-50px\); \}\n'
    r'        @keyframes flip-duck \{\n            0% \{ transform: scaleX\(1\); \}\n'
    r'            49\.9% \{ transform: scaleX\(1\); \}\n            50% \{ transform: scaleX\(-1\); \}\n'
    r'            100% \{ transform: scaleX\(-1\); \}\n        \}\n'
    r'            100% \{ transform: translateX\(50px\); \}\n        \}'
)

content = re.sub(
    search_pattern,
    r"""@keyframes swim-horizontal {
            0% { transform: translateX(-50px); }
            100% { transform: translateX(50px); }
        }

        @keyframes flip-duck {
            0% { transform: scaleX(1); }
            49.9% { transform: scaleX(1); }
            50% { transform: scaleX(-1); }
            100% { transform: scaleX(-1); }
        }""",
    content
)

# Now fix the unlurk command hitting a return early if user is undefined.
# It currently has:
# if (['!back', '!unlurk', ...].includes(textTrim)) { if (user) { ... } return; }
# Let's fix that.
old_unlurk = r"""if \(\[\'!back\', \'!unlurk\', \'!bellyflop\', \'!makeadramaticentrance\'\]\.includes\(textTrim\)\) \{
                if \(user\) \{
                    user\.isLurking = false;
                    user\.element\.classList\.remove\("lurking"\);
                    user\.element\.querySelector\('\.duck-svg'\)\.innerHTML = `<img src="assets/custom_ducks/\$\{username\}\.png" alt="\$\{username\}" style="width: 100%; height: 100%; object-fit: contain;" onerror="this\.onerror = \(\) => \{ this\.onerror = null; this\.parentElement\.innerHTML = getDuckSVG\('\$\{user\.duckColor\}'\); \}; this\.src = 'assets/custom_ducks/' \+ '\$\{username\}'\.toLowerCase\(\) \+ '\.png';" />`;
                    scatterDucks\(\);
                \}
                return;
            \}"""

# In JS, let's change it so we spawn the user if they don't exist before this unlurk block.
# But wait, we can just move this AFTER the spawn block, and remove the `return` so the message still prints.
# Or if we want it to not print, keep return but let it spawn.
# Currently, `spawnDuck` is done right below this. So let's extract it and move it after `spawnDuck`.

content = re.sub(old_unlurk, '', content)

# Wait, `spawnDuck` was moved after `unlurk`? No, let's find `let user = activeUsers.get(username);`
# It's better to just do this:
content = re.sub(
    r'(// 1\. Spawn a new duck if they aren\'t active\n            if \(!user\) \{\n                user = spawnDuck\(username, userColor\);\n                activeUsers\.set\(username, user\);\n            \})',
    r"""\1

            if (['!back', '!unlurk', '!bellyflop', '!makeadramaticentrance'].includes(textTrim)) {
                user.isLurking = false;
                user.element.classList.remove("lurking");
                user.element.querySelector('.duck-svg').innerHTML = `<img src="assets/custom_ducks/${username}.png" alt="${username}" style="width: 100%; height: 100%; object-fit: contain;" onerror="this.onerror = () => { this.onerror = null; this.parentElement.innerHTML = getDuckSVG('${user.duckColor}'); }; this.src = 'assets/custom_ducks/' + '${username}'.toLowerCase() + '.png';" />`;
                scatterDucks();
                return;
            }""",
    content
)


with open('index.html', 'w') as f:
    f.write(content)
