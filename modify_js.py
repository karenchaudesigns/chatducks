import re

with open('index.html', 'r') as f:
    content = f.read()

js_search1 = r'''            // Listen for messages
            client.on\('message', \(channel, tags, message, self\) => \{
                if \(self\) return; // Ignore own automated messages if any
                handleIncomingMessage\(tags.username, message, tags.color\);
            \}\);
        \}

        /\*\*
         \* CORE STATE MANAGEMENT
         \*/
        function handleIncomingMessage\(username, text, userColor\) \{'''

js_replace1 = '''            // Listen for messages
            client.on('message', (channel, tags, message, self) => {
                if (self) return; // Ignore own automated messages if any
                handleIncomingMessage(tags.username, message, tags.color, tags.emotes);
            });
        }

        /**
         * CORE STATE MANAGEMENT
         */
        function handleIncomingMessage(username, text, userColor, emotes) {'''

content = re.sub(js_search1, js_replace1, content)

js_search2 = r'''            user.inactivityTimer = setTimeout\(\(\) => removeDuck\(username\), INACTIVITY_LIMIT_MS\);

            // 3. Display the chat message
            showSpeechBubble\(user, text\);
        \}'''

js_replace2 = '''            user.inactivityTimer = setTimeout(() => removeDuck(username), INACTIVITY_LIMIT_MS);

            // 3. Display the chat message
            if (text.startsWith('!')) {
                showActionText(user, text, emotes);
            } else {
                showSpeechBubble(user, text, emotes);
            }
        }'''

content = re.sub(js_search2, js_replace2, content)

js_search3 = r'''            const randomDelay = \(Math.random\(\) \* 2\)\.toFixed\(2\);

            // If the user hasn't set a custom Twitch color, generate a consistent one based on their name
            const finalColor = hexColor \? hexColor : generateColorFromUsername\(username\);

            duckWrap.innerHTML = `
                <div class="bubble-container"></div>
                <div class="duck-swim" style="animation-delay: -\$\{randomDelay\}s;">
                    <div class="duck-svg">
                        <img src="assets/custom_ducks/\$\{username\}\.png" alt="\$\{username\}" style="width: 100%; height: 100%; object-fit: contain;" />
                    </div>
                    <div class="duck-name" style="color: \$\{finalColor\};">\$\{username\}</div>
                </div>
            `;'''

js_replace3 = '''            const randomDelay = (Math.random() * 2).toFixed(2);

            // Random animation delay for the flip animation (0s to 30s)
            const flipDelay = -(Math.random() * 30).toFixed(2) + 's';
            duckWrap.style.setProperty('--flip-delay', flipDelay);

            // If the user hasn't set a custom Twitch color, generate a consistent one based on their name
            const finalColor = hexColor ? hexColor : generateColorFromUsername(username);

            duckWrap.innerHTML = `
                <div class="action-container"></div>
                <div class="bubble-container"></div>
                <div class="duck-swim" style="animation-delay: -${randomDelay}s;">
                    <div class="duck-svg">
                        <img src="assets/custom_ducks/${username}.png" alt="${username}" style="width: 100%; height: 100%; object-fit: contain;" />
                    </div>
                    <div class="duck-name" style="color: ${finalColor};">${username}</div>
                </div>
            `;'''

content = re.sub(js_search3, js_replace3, content)

js_search4 = r'''                element: duckWrap,
                duckColor: finalColor,
                inactivityTimer: null,
                bubbleTimer: null,
                bubbles: \[\] // Changed from bubbleElement to bubbles array
            \};
        \}'''

js_replace4 = '''                element: duckWrap,
                duckColor: finalColor,
                inactivityTimer: null,
                bubbleTimer: null,
                bubbles: [], // Changed from bubbleElement to bubbles array
                actions: []
            };
        }'''

content = re.sub(js_search4, js_replace4, content)


js_search5 = r'''        /\*\*
         \* RENDER LOGIC: Speech Bubbles
         \*/
        function showSpeechBubble\(user, text\) \{
            const container = user.element.querySelector\('\.bubble-container'\);

            // Limit to 3 bubbles
            if \(user.bubbles.length >= 3\) \{
                const oldestBubble = user.bubbles.shift\(\);
                if \(oldestBubble && oldestBubble.parentNode\) \{
                    oldestBubble.parentNode.removeChild\(oldestBubble\);
                \}
            \}

            const isAction = text.startsWith\('!'\);
            const bubbleEl = document.createElement\('div'\);
            bubbleEl.className = isAction \? 'action-bubble' : 'speech-bubble';

            // Dynamic font sizing based on length to try and keep it within 3 lines
            // Default max-width is 200px, so very long messages need smaller font
            if \(!isAction\) \{
                if \(text.length > 100\) \{
                    bubbleEl.style.fontSize = '10px';
                \} else if \(text.length > 50\) \{
                    bubbleEl.style.fontSize = '12px';
                \}
            \}

            // Set the text. using textContent naturally escapes HTML tags, preventing malicious injection
            bubbleEl.textContent = text;

            // Append to container
            container.appendChild\(bubbleEl\);
            user.bubbles.push\(bubbleEl\);

            // Force reflow/repaint to start entrance animation
            void bubbleEl.offsetWidth;
            bubbleEl.classList.add\('active'\);

            // Start the 5-minute fade out transition immediately by removing the active class
            // after a brief delay so the entrance animation can play
            setTimeout\(\(\) => \{
                bubbleEl.classList.remove\('active'\);
                bubbleEl.classList.add\('fade-out'\);
            \}, 500\); // 500ms allows the entrance animation to finish

            // Set timer to remove bubble from DOM after fade out \(5 minutes\)
            setTimeout\(\(\) => \{
                const index = user.bubbles.indexOf\(bubbleEl\);
                if \(index > -1\) \{
                    user.bubbles.splice\(index, 1\);
                \}
                if \(bubbleEl && bubbleEl.parentNode\) \{
                    bubbleEl.remove\(\);
                \}
            \}, BUBBLE_DURATION_MS \+ 500\); // Wait for the fade out to finish
        \}'''

js_replace5 = '''        /**
         * RENDER LOGIC: Emotes parsing
         */
        function escapeHtml(unsafe) {
            return unsafe
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

        function parseEmotes(text, emotes) {
            if (!emotes) return escapeHtml(text);

            let replacements = [];
            for (const emoteId in emotes) {
                emotes[emoteId].forEach(pos => {
                    const [start, end] = pos.split('-').map(Number);
                    replacements.push({ start, end, emoteId });
                });
            }
            replacements.sort((a, b) => a.start - b.start);

            let formatted = "";
            let lastEnd = 0;
            for (const r of replacements) {
                formatted += escapeHtml(text.substring(lastEnd, r.start));
                formatted += `<img src="https://static-cdn.jtvnw.net/emoticons/v2/${r.emoteId}/default/dark/1.0" class="emote" style="vertical-align: middle; height: 1.5em;" />`;
                lastEnd = r.end + 1;
            }
            formatted += escapeHtml(text.substring(lastEnd));
            return formatted;
        }

        /**
         * RENDER LOGIC: Action Text
         */
        function showActionText(user, text, emotes) {
            const container = user.element.querySelector('.action-container');

            // Limit to 2 actions to avoid clutter
            if (user.actions.length >= 2) {
                const oldestAction = user.actions.shift();
                if (oldestAction && oldestAction.parentNode) {
                    oldestAction.parentNode.removeChild(oldestAction);
                }
            }

            const actionEl = document.createElement('div');
            actionEl.className = 'action-text';
            actionEl.innerHTML = parseEmotes(text, emotes);

            container.appendChild(actionEl);
            user.actions.push(actionEl);

            // Force reflow/repaint
            void actionEl.offsetWidth;
            actionEl.classList.add('active');

            setTimeout(() => {
                actionEl.classList.remove('active');
                actionEl.classList.add('fade-out');
            }, 500);

            setTimeout(() => {
                const index = user.actions.indexOf(actionEl);
                if (index > -1) {
                    user.actions.splice(index, 1);
                }
                if (actionEl && actionEl.parentNode) {
                    actionEl.remove();
                }
            }, BUBBLE_DURATION_MS + 500);
        }

        /**
         * RENDER LOGIC: Speech Bubbles
         */
        function showSpeechBubble(user, text, emotes) {
            const container = user.element.querySelector('.bubble-container');

            // Limit to 3 bubbles
            if (user.bubbles.length >= 3) {
                const oldestBubble = user.bubbles.shift();
                if (oldestBubble && oldestBubble.parentNode) {
                    oldestBubble.parentNode.removeChild(oldestBubble);
                }
            }

            const bubbleEl = document.createElement('div');
            bubbleEl.className = 'speech-bubble';

            if (text.length > 100) {
                bubbleEl.style.fontSize = '10px';
            } else if (text.length > 50) {
                bubbleEl.style.fontSize = '12px';
            }

            bubbleEl.innerHTML = parseEmotes(text, emotes);

            container.appendChild(bubbleEl);
            user.bubbles.push(bubbleEl);

            void bubbleEl.offsetWidth;
            bubbleEl.classList.add('active');

            setTimeout(() => {
                bubbleEl.classList.remove('active');
                bubbleEl.classList.add('fade-out');
            }, 500);

            setTimeout(() => {
                const index = user.bubbles.indexOf(bubbleEl);
                if (index > -1) {
                    user.bubbles.splice(index, 1);
                }
                if (bubbleEl && bubbleEl.parentNode) {
                    bubbleEl.remove();
                }
            }, BUBBLE_DURATION_MS + 500);
        }'''

content = re.sub(js_search5, js_replace5, content)

js_search6 = r'''            // Simulate an incoming message
            handleIncomingMessage\(username, message, null\);'''

js_replace6 = '''            // Add mock emotes for testing if it's an action or if it contains certain keywords
            let emotes = null;
            if (message.includes("PogChamp")) {
                 emotes = { "88": ["0-7"] };
            }
            if (message.includes("LUL")) {
                 emotes = { "425618": ["0-2"] };
            }
            // Simulate an incoming message
            handleIncomingMessage(username, message, null, emotes);'''

content = re.sub(js_search6, js_replace6, content)

js_search7 = r'''        const testMessages = \[
            "Quack quack!",
            "This stream is awesome! 🦆",
            "LUL",
            "PogChamp",
            "Can you explain that again\?",
            "Hello everyone!! 👋",
            "W",
            "Testing the overlay system, this is a much longer message to see how the text wrapping handles larger paragraphs."
        \];'''

js_replace7 = '''        const testMessages = [
            "Quack quack!",
            "!This stream is awesome! 🦆",
            "LUL",
            "!PogChamp",
            "Can you explain that again?",
            "Hello everyone!! 👋",
            "!W",
            "Testing the overlay system, this is a much longer message to see how the text wrapping handles larger paragraphs."
        ];'''

content = re.sub(js_search7, js_replace7, content)


with open('index.html', 'w') as f:
    f.write(content)
