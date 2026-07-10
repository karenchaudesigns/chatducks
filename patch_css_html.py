import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update timer
content = re.sub(
    r'const BUBBLE_DURATION_MS = 300000;',
    r'const BUBBLE_DURATION_MS = 150000;',
    content
)

# 2. Update CSS for .speech-bubble
search_speech_css = r'''        \.speech-bubble \{
            position: relative;
            background: white;
            color: #111827;
            padding: 10px 14px;
            border-radius: 16px;
            font-family: 'Roboto Condensed', sans-serif;
            font-size: 14px;
            font-weight: 700;
            max-width: 200px;
            word-wrap: break-word;
            text-align: center;
            box-shadow: 0 4px 15px rgba\(0,0,0,0\.3\);
            border: 3px solid #111827;
            margin-bottom: 2px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;'''

replace_speech_css = '''        .speech-bubble {
            position: relative;
            background: white;
            color: #111827;
            padding: 4px 8px;
            border-radius: 16px;
            font-family: 'Roboto Condensed', sans-serif;
            font-size: 14px;
            font-weight: 700;
            max-width: 200px;
            word-wrap: break-word;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            border: 3px solid #111827;
            margin-bottom: 0px;
            aspect-ratio: 16 / 9;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;'''
content = re.sub(search_speech_css, replace_speech_css, content)

# 3. Update CSS for .bubble-container
search_bubble_container = r'''        \.bubble-container \{
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX\(-50%\);
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            z-index: 10;
        \}'''

replace_bubble_container = '''        .bubble-container {
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            z-index: 10;
        }'''
content = re.sub(search_bubble_container, replace_bubble_container, content)

# 4. Update the tail
search_tail = r'''        /\* The tail of the speech bubble \(White fill\) \*/
        \.speech-bubble:last-child::after \{
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            border-width: 8px 8px 0;
            border-style: solid;
            border-color: white transparent transparent transparent;
            display: block;
            width: 0;
            z-index: 2;
            animation: flip-tail-after 30s infinite steps\(1\);
            animation-delay: var\(--flip-delay, 0s\);
        \}

        /\* The outline of the tail \(Black outline\) \*/
        \.speech-bubble:last-child::before \{
            content: '';
            position: absolute;
            bottom: -12px;
            left: 50%;
            border-width: 11px 11px 0;
            border-style: solid;
            border-color: #111827 transparent transparent transparent;
            display: block;
            width: 0;
            z-index: 1;
            animation: flip-tail-before 30s infinite steps\(1\);
            animation-delay: var\(--flip-delay, 0s\);
        \}'''

replace_tail = '''        /* The tail of the speech bubble (White fill) */
        .speech-bubble:last-child::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            transform: translateX(-50%);
            border-width: 8px 8px 0;
            border-style: solid;
            border-color: white transparent transparent transparent;
            display: block;
            width: 0;
            z-index: 2;
        }

        /* The outline of the tail (Black outline) */
        .speech-bubble:last-child::before {
            content: '';
            position: absolute;
            bottom: -12px;
            left: 50%;
            transform: translateX(-50%);
            border-width: 11px 11px 0;
            border-style: solid;
            border-color: #111827 transparent transparent transparent;
            display: block;
            width: 0;
            z-index: 1;
        }'''
content = re.sub(search_tail, replace_tail, content)

# 5. Move .bubble-container inside .duck-swim in spawnDuck
search_duck_html = r'''                <div class="action-container"><\/div>
                <div class="bubble-container"><\/div>
                <div class="duck-swim" style="animation-delay: -\$\{randomDelay\}s;">'''

replace_duck_html = '''                <div class="duck-swim" style="animation-delay: -${randomDelay}s;">
                    <div class="action-container"></div>
                    <div class="bubble-container"></div>'''
content = re.sub(search_duck_html, replace_duck_html, content)

# 6. Update transition durations in CSS (300s -> 150s)
content = content.replace('transition: transform 300s linear, opacity 300s linear;', 'transition: transform 150s linear, opacity 150s linear;')

# 7. Add text truncation to showSpeechBubble and showActionText
# Actually we can do it where text is passed in
search_show_speech = r'''        function showSpeechBubble\(user, text, emotes\) \{'''
replace_show_speech = '''        function showSpeechBubble(user, text, emotes) {
            if (text.length > 44) {
                text = text.substring(0, 44) + "...";
            }'''
content = re.sub(search_show_speech, replace_show_speech, content)

search_show_action = r'''        function showActionText\(user, text, emotes\) \{'''
replace_show_action = '''        function showActionText(user, text, emotes) {
            if (text.length > 44) {
                text = text.substring(0, 44) + "...";
            }'''
content = re.sub(search_show_action, replace_show_action, content)

# 8. Emote size
search_emote = r'''<img src="https://static-cdn\.jtvnw\.net/emoticons/v2/\$\{r\.emoteId\}/default/dark/1\.0" class="emote" style="vertical-align: middle; height: 1\.5em;" />'''
replace_emote = '''<img src="https://static-cdn.jtvnw.net/emoticons/v2/${r.emoteId}/default/dark/1.0" class="emote" style="vertical-align: middle; height: 2em;" />'''
content = re.sub(search_emote, replace_emote, content)

with open('index.html', 'w') as f:
    f.write(content)
