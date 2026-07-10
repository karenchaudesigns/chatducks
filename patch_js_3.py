import re

with open('index.html', 'r') as f:
    content = f.read()

# Update handleIncomingMessage front logic for StreamElements static placement re-assertion
# Bring them to front applies to normal ducks, StreamElements should stay static.
search_front = r'''            // Bring them to the front \(fast entrance animation triggers here\)
            user\.element\.style\.bottom = '5%';
            user\.element\.style\.transform = 'scale\(1\.5\)';

            // 2\. Reset their inactivity timer
            clearTimeout\(user\.inactivityTimer\);

            // Wait 2 seconds for the entrance animation to finish, then start the slow drift back
            setTimeout\(\(\) => \{
                user\.element\.classList\.add\('leaving'\);
            \}, 2000\);'''

replace_front = '''            // Bring them to the front (fast entrance animation triggers here)
            if (!user.isStatic) {
                user.element.style.bottom = '5%';
                user.element.style.transform = 'scale(1.5)';
            }

            // 2. Reset their inactivity timer
            clearTimeout(user.inactivityTimer);

            // Wait 2 seconds for the entrance animation to finish, then start the slow drift back
            if (!user.isStatic) {
                setTimeout(() => {
                    user.element.classList.add('leaving');
                }, 2000);
            }'''

content = re.sub(search_front, replace_front, content)

with open('index.html', 'w') as f:
    f.write(content)
