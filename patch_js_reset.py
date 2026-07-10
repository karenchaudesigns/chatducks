import re

with open('index.html', 'r') as f:
    content = f.read()

reset_cmd = r"""
            if (textTrim === '!shoo' || textTrim === '!reset') {
                if (tags && (tags.mod || tags.subscriber || (tags.badges && tags.badges.vip))) {
                    activeUsers.forEach(u => u.element.remove());
                    activeUsers.clear();
                    // Remove countdown ducks
                    document.querySelectorAll('.countdown-duck').forEach(el => el.remove());
                }
                return;
            }
"""

content = re.sub(
    r'(if \(textTrim === \'!clear\'\) \{)',
    reset_cmd.lstrip() + r'\n            \1',
    content
)


with open('index.html', 'w') as f:
    f.write(content)
