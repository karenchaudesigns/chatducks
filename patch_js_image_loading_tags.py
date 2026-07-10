import re

with open('index.html', 'r') as f:
    content = f.read()

# Modify handleIncomingMessage call to pass display name to ensure original casing is preserved if provided
content = re.sub(
    r'handleIncomingMessage\(tags\.username, message, tags\.color, tags\.emotes, tags\);',
    r"handleIncomingMessage(tags['display-name'] || tags.username, message, tags.color, tags.emotes, tags);",
    content
)

with open('index.html', 'w') as f:
    f.write(content)
