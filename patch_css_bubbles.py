import re

with open('index.html', 'r') as f:
    content = f.read()

# Update .speech-bubble padding, border, and remove aspect-ratio
content = re.sub(
    r'padding: 4px 8px;',
    r'padding: 8px 12px;',
    content
)
content = re.sub(
    r'border: 3px solid #111827;',
    r'border: 2px solid #111827;',
    content
)
content = re.sub(
    r'\s*aspect-ratio: 16 / 9;',
    '',
    content
)

# Update .speech-bubble:last-child::after tail (white inner)
content = re.sub(
    r'bottom: -8px;\s*left: 50%;\s*transform: translateX\(-50%\);\s*border-width: 8px 8px 0;',
    r'bottom: -6px;\n            left: 50%;\n            transform: translateX(-50%);\n            border-width: 6px 6px 0;',
    content
)

# Update .speech-bubble:last-child::before tail (black outline)
content = re.sub(
    r'bottom: -12px;\s*left: 50%;\s*transform: translateX\(-50%\);\s*border-width: 11px 11px 0;',
    r'bottom: -9px;\n            left: 50%;\n            transform: translateX(-50%);\n            border-width: 9px 9px 0;',
    content
)


with open('index.html', 'w') as f:
    f.write(content)
