import re

def update_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # 1. Update BUBBLE_DURATION_MS
    content = re.sub(
        r'const BUBBLE_DURATION_MS = \d+;',
        r'const BUBBLE_DURATION_MS = 150000;',
        content
    )

    # 2. Add scatterDucks and handle tags
    # Also update handleIncomingMessage signature to receive tags
    content = re.sub(
        r"handleIncomingMessage\(tags\.username, message, tags\.color, tags\.emotes\);",
        r"handleIncomingMessage(tags.username, message, tags.color, tags.emotes, tags);",
        content
    )

    handle_in_search = r'function handleIncomingMessage\(username, text, userColor, emotes\) \{'
    handle_in_replace = r'''function scatterDucks() {
            const activeDucks = Array.from(activeUsers.values()).filter(u => !u.isLurking && !u.isStatic);
            const count = activeDucks.length;
            if (count === 0) return;
            const step = 80 / count;
            activeDucks.forEach((u, i) => {
                u.element.style.left = `${10 + (i * step) + (Math.random() * step * 0.5)}%`;
            });
        }

        function handleIncomingMessage(username, text, userColor, emotes, tags) {
            text = text.trim();
            if (text === '!scatter') {
                scatterDucks();
                return;
            }
            if (text === '!clear' && tags && (tags.mod || tags.subscriber || (tags.badges && tags.badges.vip))) {
                activeUsers.forEach(u => {
                    u.bubbles.forEach(b => b.remove());
                    u.actions.forEach(a => a.remove());
                    u.bubbles = [];
                    u.actions = [];
                });
                return;
            }
            if (text === '!lurk' || (emotes && Object.keys(emotes).some(id => id === 'karenc9Lurkyduck'))) { // Assuming emote name checking isn't id based, wait, tmi gives IDs.
                // Let's rely on text or if someone types karenc9Lurkyduck. Actually, if they use the emote, it's in text.
                // Re-evaluate: "karenc9Lurkyduck" will just be in the text string, even if parsed as emote.
            }
'''
    # We will refine this python script later, this is just to test bash multiline.
    pass
