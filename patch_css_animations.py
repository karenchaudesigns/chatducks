import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace flip-duck animation on duck-svg
content = re.sub(
    r'animation: flip-duck 30s infinite steps\(1\);',
    '',
    content
)

# Remove @keyframes flip-duck entirely
content = re.sub(
    r'@keyframes flip-duck \{\s*0% \{ transform: scaleX\(1\); \}\s*50% \{ transform: scaleX\(-1\); \}\s*100% \{ transform: scaleX\(1\); \}\s*\}',
    '',
    content
)

# Update @keyframes swim-horizontal
new_swim = """@keyframes swim-horizontal {
            0% { transform: translateX(-50px) scaleX(1); }
            49.9% { transform: translateX(50px) scaleX(1); }
            50% { transform: translateX(50px) scaleX(-1); }
            100% { transform: translateX(-50px) scaleX(-1); }
        }"""
content = re.sub(
    r'@keyframes swim-horizontal \{\s*0% \{ transform: translateX\(-50px\); \}\s*100% \{ transform: translateX\(50px\); \}\s*\}',
    new_swim,
    content
)

# Update .duck-swim to remove alternate
content = re.sub(
    r'animation: swim-horizontal 15s infinite linear alternate;',
    r'animation: swim-horizontal 30s infinite linear;',
    content
)

# Add .lurking class at the end of duck styling
lurking_css = """
        .lurking .duck-swim, .lurking .duck-svg, .lurking .action-text {
            animation: none !important;
        }
        .lurking .duck-svg {
            transform: scaleX(1) !important;
        }
"""
content = re.sub(
    r'(/\* === SPEECH BUBBLES === \*/)',
    lurking_css + r'\n        \1',
    content
)

with open('index.html', 'w') as f:
    f.write(content)
