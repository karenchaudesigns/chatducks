import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update CSS
css_search = r'''        #pond \{
            position: absolute;
            bottom: -50px;
            left: 5%;
            width: 90%;
            height: 250px;
            background-color: rgba\(173, 216, 230, 0\.6\);
            border-radius: 50% 50% 0 0;
            pointer-events: none; /\* Let clicks pass through if used over other elements \*/
        \}'''

css_replace = '''        #pond {
            position: absolute;
            bottom: -50px;
            left: 5%;
            width: 90%;
            height: 250px;
            pointer-events: none; /* Let clicks pass through if used over other elements */
        }

        #pond-bg {
            position: absolute;
            bottom: -50px;
            left: 5%;
            width: 90%;
            height: 250px;
            pointer-events: none;
            z-index: -1;
        }'''

content = re.sub(css_search, css_replace, content)

# 2. Update HTML
html_search = r'''    <div id="pond-sign">Chat Pond</div>
    <div id="pond"></div>'''

html_replace = '''    <div id="pond-sign">Chat Pond</div>

    <svg id="pond-bg" viewBox="0 0 1000 300" preserveAspectRatio="none">
        <!-- Kidney Bean Pond -->
        <path d="M 100 150
                 C 100 0, 900 0, 900 150
                 C 900 300, 700 200, 500 200
                 C 300 200, 100 300, 100 150 Z"
              fill="#5EBDDB" />

        <!-- Left Grass -->
        <path d="M 90 140 Q 60 100 50 150 Q 70 160 90 140 Z" fill="#2E7D32" />
        <path d="M 105 130 Q 80 80 70 140 Q 90 150 105 130 Z" fill="#388E3C" />

        <!-- Right Stones -->
        <ellipse cx="880" cy="220" rx="40" ry="20" fill="#7F8C8D" />
        <ellipse cx="920" cy="240" rx="35" ry="15" fill="#95A5A6" />
        <ellipse cx="850" cy="250" rx="25" ry="12" fill="#7F8C8D" />

        <!-- Top Right Cattails -->
        <g transform="translate(800, 20)">
            <path d="M 20 80 Q 15 40 10 0" stroke="#2E7D32" stroke-width="4" fill="none" />
            <rect x="7" y="10" width="6" height="30" rx="3" fill="#5D4037" />
            <path d="M 40 90 Q 45 50 50 10" stroke="#2E7D32" stroke-width="4" fill="none" />
            <rect x="47" y="20" width="6" height="30" rx="3" fill="#5D4037" />
        </g>
    </svg>
    <div id="pond"></div>'''

content = re.sub(html_search, html_replace, content)

with open('index.html', 'w') as f:
    f.write(content)
