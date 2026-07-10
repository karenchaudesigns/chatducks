import re

with open('index.html', 'r') as f:
    content = f.read()

# I accidentally stripped the `animation: flip-duck 30s infinite linear;` from `.duck-svg` in the previous step. Let's add it back correctly.
content = re.sub(
    r'(\.duck-svg \{\n            width: 80px;\n            height: 80px;\n            \n            animation-delay: var\(--flip-delay, 0s\);\n            filter: drop-shadow\(0px 8px 6px rgba\(0,0,0,0\.4\)\);)\}',
    r'\1\n            animation: flip-duck 30s infinite steps(1);\n        }',
    content
)

# Wait, `steps(1)` is what the original had, or we can use `linear` if the keyframes are step-like (0%, 49.9%, 50%, 100%).
# Let's use `animation: flip-duck 30s infinite linear;` but since we used 49.9% and 50% it will act like steps.
content = re.sub(
    r'animation: flip-duck 30s infinite steps\(1\);',
    r'animation: flip-duck 30s infinite linear;',
    content
)

# Check if it was applied
if 'animation: flip-duck' not in content:
    # Manual fallback
    content = content.replace(
        'filter: drop-shadow(0px 8px 6px rgba(0,0,0,0.4));}',
        'filter: drop-shadow(0px 8px 6px rgba(0,0,0,0.4));\n            animation: flip-duck 30s infinite linear;\n        }'
    )

with open('index.html', 'w') as f:
    f.write(content)
