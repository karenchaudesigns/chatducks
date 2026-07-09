import re

with open('index.html', 'r') as f:
    content = f.read()

search = r'''        \.action-text \{
            font-family: 'Roboto Condensed', sans-serif;
            font-size: 18px;
            font-style: italic;
            font-weight: bold;
            color: #d84315;
            background: #ffeb3b;
            padding: 4px 8px;
            border-radius: 8px;
            border: 2px solid #d84315;
            box-shadow: 0 2px 8px rgba\(0,0,0,0\.3\);'''

replace = '''        .action-text {
            font-family: 'Roboto Condensed', sans-serif;
            font-size: 20px;
            font-style: italic;
            font-weight: 900;
            color: #ffeb3b;
            text-shadow: -1px -1px 0 #d84315, 1px -1px 0 #d84315, -1px 1px 0 #d84315, 1px 1px 0 #d84315, 0 2px 4px rgba(0,0,0,0.5);'''

content = re.sub(search, replace, content)

with open('index.html', 'w') as f:
    f.write(content)
