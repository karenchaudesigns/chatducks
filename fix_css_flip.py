import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the swim animation to only translate
new_swim = r"""@keyframes swim-horizontal {
            0% { transform: translateX(-50px); }
            100% { transform: translateX(50px); }
        }"""
content = re.sub(
    r'@keyframes swim-horizontal \{\s*0% \{ transform: translateX\(-50px\) scaleX\(1\); \}\s*49\.9% \{ transform: translateX\(50px\) scaleX\(1\); \}\s*50% \{ transform: translateX\(50px\) scaleX\(-1\); \}\s*100% \{ transform: translateX\(-50px\) scaleX\(-1\); \}\s*\}',
    new_swim,
    content
)

# Put the flip animation back, but apply it to .duck-svg directly with the correct timing so it only flips the image, not the text!
content = re.sub(
    r'(\.duck-svg \{[\s\S]*?)(\})',
    r'\1    animation: flip-duck 30s infinite linear;\n\2',
    content
)

new_flip = r"""
        @keyframes flip-duck {
            0% { transform: scaleX(1); }
            49.9% { transform: scaleX(1); }
            50% { transform: scaleX(-1); }
            100% { transform: scaleX(-1); }
        }"""
content = re.sub(
    r'(@keyframes swim-horizontal \{[\s\S]*?\})',
    r'\1' + new_flip,
    content
)

with open('index.html', 'w') as f:
    f.write(content)
