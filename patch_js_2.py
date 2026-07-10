import re

with open('index.html', 'r') as f:
    content = f.read()

# Modify spawnDuck to handle StreamElements and scatter at the end
search_spawn = r'''            return \{
                element: duckWrap,
                duckColor: finalColor,
                inactivityTimer: null,
                bubbleTimer: null,
                bubbles: \[\], // Changed from bubbleElement to bubbles array
                actions: \[\]
            \};'''

replace_spawn = '''            const userObj = {
                element: duckWrap,
                duckColor: finalColor,
                inactivityTimer: null,
                bubbleTimer: null,
                bubbles: [],
                actions: [],
                isStatic: false,
                isLurking: false
            };

            if (username.toLowerCase() === 'streamelements') {
                userObj.isStatic = true;
                setTimeout(() => {
                    duckWrap.style.left = '85%';
                    duckWrap.style.bottom = '90%';
                    duckWrap.style.transform = 'scale(0.6)';
                }, 150);
            } else {
                setTimeout(() => {
                    if (typeof scatterDucks === 'function') {
                        scatterDucks();
                    }
                }, 150);
            }

            return userObj;'''

content = re.sub(search_spawn, replace_spawn, content)

# Modify spawnDuck return and handle StreamElements initial placement inside setTimeout
search_spawn_timeout = r'''            setTimeout\(\(\) => \{
                const targetLeft = Math\.random\(\) \* 80 \+ 10;
                duckWrap\.style\.left = `\$\{targetLeft\}%`;
            \}, 100\);'''

replace_spawn_timeout = '''            setTimeout(() => {
                const targetLeft = Math.random() * 80 + 10;
                duckWrap.style.left = `${targetLeft}%`;
            }, 100);'''

# Actually, the above targetLeft is what we replace with scatterDucks eventually, but scatterDucks covers it.
# Let's just write to file.
with open('index.html', 'w') as f:
    f.write(content)
