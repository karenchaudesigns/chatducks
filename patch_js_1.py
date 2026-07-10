import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update event listener to pass tags
content = content.replace(
    '''            client.on('message', (channel, tags, message, self) => {
                if (self) return; // Ignore own automated messages if any
                handleIncomingMessage(tags.username, message, tags.color, tags.emotes);
            });''',
    '''            client.on('message', (channel, tags, message, self) => {
                if (self) return; // Ignore own automated messages if any
                handleIncomingMessage(tags.username, message, tags.color, tags.emotes, tags);
            });'''
)

# 2. Update handleIncomingMessage signature & logic
search_handle = r'''        function handleIncomingMessage\(username, text, userColor, emotes\) \{
            let user = activeUsers\.get\(username\);

            // 1\. Spawn a new duck if they aren't active
            if \(!user\) \{
                user = spawnDuck\(username, userColor\);
                activeUsers\.set\(username, user\);
            \}'''

replace_handle = '''        function scatterDucks() {
            const activeDucks = Array.from(activeUsers.values()).filter(u => !u.isLurking && !u.isStatic);
            const count = activeDucks.length;
            if (count === 0) return;
            const step = 80 / count;
            activeDucks.forEach((u, i) => {
                const targetLeft = 10 + (i * step) + (Math.random() * step * 0.5);
                u.element.style.left = `${targetLeft}%`;
            });
        }

        function handleIncomingMessage(username, text, userColor, emotes, tags) {
            let textTrim = text.trim();
            if (textTrim === '!scatter') {
                scatterDucks();
                return;
            }
            if (textTrim === '!clear') {
                if (tags && (tags.mod || tags.subscriber || (tags.badges && tags.badges.vip))) {
                    activeUsers.forEach(u => {
                        u.bubbles.forEach(b => b.remove());
                        u.actions.forEach(a => a.remove());
                        u.bubbles = [];
                        u.actions = [];
                    });
                }
                return;
            }

            let user = activeUsers.get(username);

            // 1. Spawn a new duck if they aren't active
            if (!user) {
                user = spawnDuck(username, userColor);
                activeUsers.set(username, user);
            }

            // LURK AND UNLURK SYSTEM
            const isLurkEmote = emotes && Object.values(emotes).some(posArr => text.substring(posArr[0].split('-')[0], posArr[0].split('-')[1]).includes('karenc9Lurkyduck'));
            if (textTrim === '!lurk' || text.includes('karenc9Lurkyduck')) {
                user.isLurking = true;
                user.lurkTime = Date.now();
                if (!user.originalImage) {
                    user.originalImage = user.element.querySelector('.duck-svg').innerHTML;
                }
                user.element.querySelector('.duck-svg').innerHTML = `<img src="custom_ducks/lurkyduck.png" alt="lurkyduck" style="width: 100%; height: 100%; object-fit: contain;" />`;
                user.element.style.transform = 'scale(0.6)';
                user.element.style.bottom = '90%';
                user.element.style.left = Math.random() > 0.5 ? '5%' : '95%';
                clearTimeout(user.inactivityTimer);
                return; // Stop processing further for lurk
            }

            if (user.isLurking) {
                if (Date.now() - user.lurkTime > 300000) {
                    user.isLurking = false;
                    if (user.originalImage) {
                        user.element.querySelector('.duck-svg').innerHTML = user.originalImage;
                    }
                    // Scatter handles repositioning later, but reset scale and let it re-animate
                    scatterDucks();
                } else {
                    return; // Ignore messages if they are still lurking within 5 mins
                }
            }'''

content = re.sub(search_handle, replace_handle, content)

with open('index.html', 'w') as f:
    f.write(content)
