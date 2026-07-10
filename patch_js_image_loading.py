import re

with open('index.html', 'r') as f:
    content = f.read()

# Update handleIncomingMessage signature to pass down tags to spawnDuck if needed, but actually we can just pass the raw username with original case
# The tmi tag display-name preserves case, but tmi.js username tag might already be lowercased depending on the version. Let's make spawnDuck robust.

# Update img tag inside spawnDuck
old_img = r'<img src="custom_ducks/\$\{username\}\.png" alt="\$\{username\}" style="width: 100%; height: 100%; object-fit: contain;" />'
new_img = r"""<img src="custom_ducks/${username}.png" alt="${username}" style="width: 100%; height: 100%; object-fit: contain;" onerror="this.onerror = () => { this.onerror = null; this.parentElement.innerHTML = getDuckSVG('${finalColor}'); }; this.src = 'custom_ducks/' + '${username}'.toLowerCase() + '.png';" />"""

content = re.sub(old_img, new_img, content)

# Remove the old img.onerror logic below it
content = re.sub(
    r'const img = duckWrap\.querySelector\(\'img\'\);\s*img\.onerror = \(\) => \{\s*img\.parentElement\.innerHTML = getDuckSVG\(finalColor\);\s*\};\s*',
    '',
    content
)


with open('index.html', 'w') as f:
    f.write(content)
