import re

with open('index.html', 'r') as f:
    content = f.read()

# Remove .action-bubble and update .speech-bubble
css_search1 = r'''        \.speech-bubble, \.action-bubble \{
            position: relative;
            background: white;
            color: #111827;
            padding: 10px 14px;
            border-radius: 16px;
            font-family: 'Roboto Condensed', sans-serif;
            font-size: 14px; /\* Default size, JS might override \*/
            font-weight: 700;
            max-width: 200px;
            word-wrap: break-word;
            text-align: center;
            box-shadow: 0 4px 15px rgba\(0,0,0,0\.3\);
            border: 3px solid #111827;
            margin-bottom: 5px; /\* Tighter for cascading \*/

            /\* To limit to max 3 lines \*/
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;

            /\* Hidden by default, animated in \*/
            opacity: 0;
            transform: translateY\(10px\) scale\(0\.8\);
            transform-origin: bottom center;
            /\* Fast entrance transition \*/
            transition: transform 0\.3s cubic-bezier\(0\.175, 0\.885, 0\.32, 1\.275\), opacity 0\.3s linear;
        \}

        \.action-bubble \{
            background: #ffeb3b;
            color: #d84315;
            border-color: #d84315;
            font-size: 18px; /\* Slightly larger by default for actions \*/
            font-style: italic;
        \}

        \.speech-bubble\.active, \.action-bubble\.active,
        \.speech-bubble\.fade-out, \.action-bubble\.fade-out \{
            transform: translateY\(0\) scale\(1\);
        \}

        \.speech-bubble\.active, \.action-bubble\.active \{
            opacity: 1;
        \}

        \.speech-bubble\.fade-out, \.action-bubble\.fade-out \{
            opacity: 0;
            /\* Fade transition set to 300s \(5 minutes\) for fading out over time \*/
            transition: transform 0\.3s cubic-bezier\(0\.175, 0\.885, 0\.32, 1\.275\), opacity 300s linear;
        \}'''

css_replace1 = '''        .speech-bubble {
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
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            border: 3px solid #111827;
            margin-bottom: 5px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            opacity: 0;
            transform: translateY(10px) scale(0.8);
            transform-origin: bottom center;
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s linear;
        }

        .action-container {
            position: absolute;
            bottom: 50%; /* Near back of the duck */
            left: 50%;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            z-index: 10;
        }

        .action-text {
            font-family: 'Roboto Condensed', sans-serif;
            font-size: 18px;
            font-style: italic;
            font-weight: bold;
            color: #d84315;
            background: #ffeb3b;
            padding: 4px 8px;
            border-radius: 8px;
            border: 2px solid #d84315;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            margin-bottom: 5px;
            opacity: 0;
            transform: translateY(10px) scale(0.8);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s linear;

            /* Animate to flip sides with the duck */
            animation: flip-action 30s infinite steps(1);
            animation-delay: var(--flip-delay, 0s);
        }

        .speech-bubble.active, .action-text.active {
            transform: translateY(0) scale(1);
            opacity: 1;
        }

        .speech-bubble.fade-out, .action-text.fade-out {
            opacity: 0;
            transform: translateY(0) scale(0);
            transition: transform 300s linear, opacity 300s linear;
        }'''

content = re.sub(css_search1, css_replace1, content)

css_search2 = r'''        /\* The tail of the speech bubble \(White fill\) \*/
        \.speech-bubble:last-child::after, \.action-bubble:last-child::after \{
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            transform: translateX\(-50%\);
            border-width: 8px 8px 0;
            border-style: solid;
            border-color: white transparent transparent transparent;
            display: block;
            width: 0;
            z-index: 2;
        \}

        \.action-bubble:last-child::after \{
            border-color: #ffeb3b transparent transparent transparent;
        \}

        /\* The outline of the tail \(Black outline\) \*/
        \.speech-bubble:last-child::before, \.action-bubble:last-child::before \{
            content: '';
            position: absolute;
            bottom: -12px;
            left: 50%;
            transform: translateX\(-50%\);
            border-width: 11px 11px 0;
            border-style: solid;
            border-color: #111827 transparent transparent transparent;
            display: block;
            width: 0;
            z-index: 1;
        \}

        \.action-bubble:last-child::before \{
             border-color: #d84315 transparent transparent transparent;
        \}'''

css_replace2 = '''        /* The tail of the speech bubble (White fill) */
        .speech-bubble:last-child::after {
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
            animation: flip-tail-after 30s infinite steps(1);
            animation-delay: var(--flip-delay, 0s);
        }

        /* The outline of the tail (Black outline) */
        .speech-bubble:last-child::before {
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
            animation: flip-tail-before 30s infinite steps(1);
            animation-delay: var(--flip-delay, 0s);
        }'''

content = re.sub(css_search2, css_replace2, content)


css_search3 = r'''        \.duck-svg \{
            width: 80px;
            height: 80px;
            animation: flip-duck 30s infinite steps\(1\);
            filter: drop-shadow\(0px 8px 6px rgba\(0,0,0,0\.4\)\);
        \}'''

css_replace3 = '''        .duck-svg {
            width: 80px;
            height: 80px;
            animation: flip-duck 30s infinite steps(1);
            animation-delay: var(--flip-delay, 0s);
            filter: drop-shadow(0px 8px 6px rgba(0,0,0,0.4));
        }'''

content = re.sub(css_search3, css_replace3, content)

css_search4 = r'''        @keyframes flip-duck \{
            0% \{ transform: scaleX\(1\); \}
            50% \{ transform: scaleX\(-1\); \}
            100% \{ transform: scaleX\(1\); \}
        \}'''

css_replace4 = '''        @keyframes flip-duck {
            0% { transform: scaleX(1); }
            50% { transform: scaleX(-1); }
            100% { transform: scaleX(1); }
        }

        @keyframes flip-action {
            /* Flip the action text so it stays near the tail */
            0% { transform: translateX(-100%); } /* Left tail */
            50% { transform: translateX(100%); } /* Right tail */
            100% { transform: translateX(-100%); }
        }

        @keyframes flip-tail-after {
            /* Skew tail toward duck bill */
            /* duck faces right at 0%, bill is to the right */
            0% { transform: translateX(-50%) skewX(-30deg); left: 75%; }
            /* duck faces left at 50%, bill is to the left */
            50% { transform: translateX(-50%) skewX(30deg); left: 25%; }
            100% { transform: translateX(-50%) skewX(-30deg); left: 75%; }
        }

        @keyframes flip-tail-before {
            /* Skew tail outline toward duck bill */
            0% { transform: translateX(-50%) skewX(-30deg); left: 75%; }
            50% { transform: translateX(-50%) skewX(30deg); left: 25%; }
            100% { transform: translateX(-50%) skewX(-30deg); left: 75%; }
        }'''

content = re.sub(css_search4, css_replace4, content)

with open('index.html', 'w') as f:
    f.write(content)
