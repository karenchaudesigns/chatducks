import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix the action text emote string manipulation issue.
# Twitch emotes indices map to the exact original string.
# We shouldn't manipulate the string *before* parsing emotes.
search = r'''        function showActionText\(user, text, emotes\) \{
            text = text.replace\(\/\^\!\/, ''\); // Remove the leading ! so emotes index map properly or don't render oddly
            const container = user.element.querySelector\('\.action-container'\);'''

replace = '''        function showActionText(user, text, emotes) {
            const container = user.element.querySelector('.action-container');'''

content = re.sub(search, replace, content)

with open('index.html', 'w') as f:
    f.write(content)
