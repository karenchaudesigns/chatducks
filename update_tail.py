import re

with open('index.html', 'r') as f:
    content = f.read()

search = r'''        @keyframes flip-tail-after \{
            /\* Skew tail toward duck bill \*/
            /\* duck faces right at 0%, bill is to the right \*/
            0% \{ transform: translateX\(-50%\) skewX\(-30deg\); left: 75%; \}
            /\* duck faces left at 50%, bill is to the left \*/
            50% \{ transform: translateX\(-50%\) skewX\(30deg\); left: 25%; \}
            100% \{ transform: translateX\(-50%\) skewX\(-30deg\); left: 75%; \}
        \}

        @keyframes flip-tail-before \{
            /\* Skew tail outline toward duck bill \*/
            0% \{ transform: translateX\(-50%\) skewX\(-30deg\); left: 75%; \}
            50% \{ transform: translateX\(-50%\) skewX\(30deg\); left: 25%; \}
            100% \{ transform: translateX\(-50%\) skewX\(-30deg\); left: 75%; \}
        \}'''

replace = '''        @keyframes flip-tail-after {
            /* duck faces right at 0%, bill is to the right, point tail to bill -> right side */
            0% { transform: translateX(-50%) skewX(-30deg); left: 65%; }
            /* duck faces left at 50%, bill is to the left, point tail to bill -> left side */
            50% { transform: translateX(-50%) skewX(30deg); left: 35%; }
            100% { transform: translateX(-50%) skewX(-30deg); left: 65%; }
        }

        @keyframes flip-tail-before {
            0% { transform: translateX(-50%) skewX(-30deg); left: 65%; }
            50% { transform: translateX(-50%) skewX(30deg); left: 35%; }
            100% { transform: translateX(-50%) skewX(-30deg); left: 65%; }
        }'''

content = re.sub(search, replace, content)

with open('index.html', 'w') as f:
    f.write(content)
