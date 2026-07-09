import re

with open('index.html', 'r') as f:
    content = f.read()

# Make sure action text has space to breathe, the image wasn't rendering in the !PogChamp due to ! character index offset
search = r'''        function showActionText\(user, text, emotes\) \{'''
replace = '''        function showActionText(user, text, emotes) {
            text = text.replace(/^!/, ''); // Remove the leading ! so emotes index map properly or don't render oddly'''
content = re.sub(search, replace, content)

with open('index.html', 'w') as f:
    f.write(content)
