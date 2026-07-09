        /**
         * CONFIGURATION
         */
        const INACTIVITY_LIMIT_MS = 60000 * 10; // 10 minutes. Ducks leave if silent this long.
        const BUBBLE_DURATION_MS = 300000;      // 5 minutes. How long chat bubbles stay up.

        let client = null; // tmi.js client
        const activeUsers = new Map(); // Stores { element, duckColor, inactivityTimer, bubbleTimer }
        const pond = document.getElementById('pond');
        const setupModal = document.getElementById('setup-modal');
        const statusMsg = document.getElementById('status-msg');

        /**
         * DYNAMIC SCRIPT LOADER WITH FALLBACKS
         */
        const TMI_CDNS = [
            'tmi.min.js'
        ];

        function loadTmi(callback, attempt = 0) {
            if (typeof tmi !== 'undefined') {
                callback();
                return;
            }

            if (attempt >= TMI_CDNS.length) {
                statusMsg.style.display = 'block';
                statusMsg.style.color = '#ef4444';
                statusMsg.innerText = "Error: Blocked from loading Twitch library. Try disabling adblockers/privacy shields for this page.";
                return;
            }

            const script = document.createElement('script');
            script.src = TMI_CDNS[attempt];
            script.onload = callback;
            script.onerror = () => {
                console.warn(`Failed to load tmi.js from ${TMI_CDNS[attempt]}, trying fallback...`);
                loadTmi(callback, attempt + 1);
            };
            document.head.appendChild(script);
        }

        /**
         * INITIALIZATION & URL PARSING
         */
        window.onload = () => {
            const params = new URLSearchParams(window.location.search);
            const channelParam = params.get('channel');

            if (channelParam) {
                // If loaded via OBS with a parameter, skip UI and connect instantly
                setupModal.style.display = 'none';
                loadTmi(() => connectToTwitch(channelParam));
            }
        };

        function startConnection() {
            const channel = document.getElementById('channel-input').value.trim();
            if (!channel) return;

            statusMsg.style.display = 'block';
            statusMsg.style.color = '#34d399';
            statusMsg.innerText = `Loading libraries...`;

            loadTmi(() => {
                statusMsg.innerText = `Connecting to #${channel}...`;
                connectToTwitch(channel);
            });
        }

        /**
         * TWITCH CONNECTION LOGIC
         */
        function connectToTwitch(channel) {
            // Remove the # if they added it
            channel = channel.replace('#', '');

            client = new tmi.Client({
                channels: [channel]
            });

            client.connect().then(() => {
                // Successfully connected
                setupModal.style.opacity = '0';
                setTimeout(() => {
                    setupModal.style.display = 'none';
                }, 500);
            }).catch(console.error);

            // Listen for messages
            client.on('message', (channel, tags, message, self) => {
                if (self) return; // Ignore own automated messages if any
                handleIncomingMessage(tags.username, message, tags.color, tags.emotes);
            });
        }

        /**
         * CORE STATE MANAGEMENT
         */
        function handleIncomingMessage(username, text, userColor, emotes) {
            let user = activeUsers.get(username);

            // 1. Spawn a new duck if they aren't active
            if (!user) {
                user = spawnDuck(username, userColor);
                activeUsers.set(username, user);
            }

            // Immediately reset opacity and clear leaving transition if they were fading
            user.element.classList.remove('leaving');
            // Temporarily disable transition so opacity snaps back to 1 instantly
            user.element.style.transition = 'none';

            // 2. Reset their inactivity timer
            clearTimeout(user.inactivityTimer);

            // Give the browser a tick to register opacity=1 before applying the 10 minute fade out
            setTimeout(() => {
                user.element.style.transition = ''; // Restore original transitions
                user.element.classList.add('leaving');
            }, 50);

            user.inactivityTimer = setTimeout(() => removeDuck(username), INACTIVITY_LIMIT_MS);

            // 3. Display the chat message
            if (text.startsWith('!')) {
                showActionText(user, text, emotes);
            } else {
                showSpeechBubble(user, text, emotes);
            }
        }

        /**
         * RENDER LOGIC: Spawning Ducks
         */
        function spawnDuck(username, hexColor) {
            const duckWrap = document.createElement('div');
            duckWrap.className = 'duck-wrapper';

            // Randomize the swimming animation start time slightly
            const randomDelay = (Math.random() * 2).toFixed(2);

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
                        <img src="custom_ducks/${username}.png" alt="${username}" style="width: 100%; height: 100%; object-fit: contain;" />
                    </div>
                    <div class="duck-name" style="color: ${finalColor};">${username}</div>
                </div>
            `;

            const img = duckWrap.querySelector('img');
            img.onerror = () => {
                img.parentElement.innerHTML = getDuckSVG(finalColor);
            };

            // Randomly choose an edge to spawn from: 0=left, 1=right, 2=bottom
            const edge = Math.floor(Math.random() * 3);
            if (edge === 0) {
                duckWrap.style.left = '-100px';
                duckWrap.style.bottom = `${Math.random() * 80 + 10}%`; // random height in pond
            } else if (edge === 1) {
                duckWrap.style.left = 'calc(100% + 100px)';
                duckWrap.style.bottom = `${Math.random() * 80 + 10}%`;
            } else {
                duckWrap.style.left = `${Math.random() * 80 + 10}%`;
                duckWrap.style.bottom = '-100px';
            }

            pond.appendChild(duckWrap);

            // Allow DOM to update then move to random position inside pond
            setTimeout(() => {
                const targetLeft = Math.random() * 80 + 10;
                const targetBottom = Math.random() * 50 + 10;
                duckWrap.style.left = `${targetLeft}%`;
                duckWrap.style.bottom = `${targetBottom}%`;
            }, 100);

            return {
                element: duckWrap,
                duckColor: finalColor,
                inactivityTimer: null,
                bubbleTimer: null,
                bubbles: [], // Changed from bubbleElement to bubbles array
                actions: []
            };
        }

        /**
         * RENDER LOGIC: Removing Ducks
         */
        function removeDuck(username) {
            const user = activeUsers.get(username);
            if (!user) return;

            // Remove from DOM once fully faded
            user.element.remove();
            activeUsers.delete(username);
        }

        /**
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
        }

        /**
         * UTILITY: Generate a nice SVG Duck dynamically
         */
        function getDuckSVG(color) {
            return `
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
                <g stroke="#111827" stroke-width="3" stroke-linejoin="round">
                    <!-- Tail -->
                    <path d="M 25 55 L 5 40 L 20 70 Z" fill="${color}" />
                    <!-- Body -->
                    <ellipse cx="45" cy="65" rx="35" ry="25" fill="${color}" />
                    <!-- Head -->
                    <circle cx="65" cy="35" r="22" fill="${color}" />
                    <!-- Beak Top -->
                    <path d="M 85 30 Q 105 30 98 38 L 85 38 Z" fill="#FFB300" />
                    <!-- Beak Bottom -->
                    <path d="M 85 38 L 96 38 Q 96 44 85 43 Z" fill="#F39C12" />
                    <!-- Wing -->
                    <path d="M 35 60 Q 55 50 65 65 Q 45 75 35 60 Z" fill="rgba(0,0,0,0.1)" stroke="rgba(0,0,0,0.2)" stroke-width="2"/>
                </g>
                <!-- Eye -->
                <circle cx="72" cy="28" r="3.5" fill="#111827" />
                <circle cx="73" cy="27" r="1" fill="#FFFFFF" /> <!-- Eye glint -->
            </svg>`;
        }

        /**
         * UTILITY: Hashing function to ensure returning users get the same duck color
         */
        function generateColorFromUsername(str) {
            let hash = 0;
            for (let i = 0; i < str.length; i++) {
                hash = str.charCodeAt(i) + ((hash << 5) - hash);
            }

            // To make sure ducks are brightly colored and visible, we use HSL
            const hue = Math.abs(hash % 360);
            // Saturation 70-100%, Lightness 50-70% for vibrant, pastel-ish colors
            return `hsl(${hue}, 85%, 60%)`;
        }

        /**
         * TESTING: Generate fake messages for OBS setup
         */
        const testMessages = [
            "Quack quack!",
            "!This stream is awesome! 🦆",
            "LUL",
            "!PogChamp",
            "Can you explain that again?",
            "Hello everyone!! 👋",
            "!W",
            "Testing the overlay system, this is a much longer message to see how the text wrapping handles larger paragraphs."
        ];

        let testCounter = 1;

        function spawnTestMessage() {
            // Close the modal to show the ducks
            if (setupModal.style.display !== 'none') {
                setupModal.style.opacity = '0';
                setTimeout(() => setupModal.style.display = 'none', 500);
            }

            const username = `TestUser_${testCounter}`;
            const message = testMessages[Math.floor(Math.random() * testMessages.length)];

            // Add mock emotes for testing if it's an action or if it contains certain keywords
            let emotes = null;
            if (message.includes("PogChamp")) {
                 emotes = { "88": ["0-7"] };
            }
            if (message.includes("LUL")) {
                 emotes = { "425618": ["0-2"] };
            }
            // Simulate an incoming message
            handleIncomingMessage(username, message, null, emotes);

            testCounter++;
            if (testCounter > 10) testCounter = 1;
        }
