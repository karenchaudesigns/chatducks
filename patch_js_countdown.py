import re

with open('index.html', 'r') as f:
    content = f.read()

countdown_cmd = r"""
            if (textTrim.startsWith('!countdown ')) {
                const duration = parseInt(textTrim.split(' ')[1]);
                if (!isNaN(duration) && duration > 0) {
                    const duckWrap = document.createElement('div');
                    duckWrap.className = 'duck-wrapper countdown-duck';
                    duckWrap.style.left = '5%';
                    duckWrap.style.bottom = '5%';
                    duckWrap.style.transform = 'scale(1.5)';
                    duckWrap.style.zIndex = ++globalZIndex;

                    const finalColor = generateColorFromUsername(username);

                    duckWrap.innerHTML = `
                        <div class="duck-swim" style="animation: none !important;">
                            <div class="bubble-container"></div>
                            <div class="duck-svg" style="transform: scaleX(1) !important;">
                                <img src="assets/custom_ducks/${username}.png" alt="${username}" style="width: 100%; height: 100%; object-fit: contain;" onerror="this.onerror = () => { this.onerror = null; this.parentElement.innerHTML = getDuckSVG('${finalColor}'); }; this.src = 'assets/custom_ducks/' + '${username}'.toLowerCase() + '.png';" />
                            </div>
                            <div class="duck-name" style="color: ${finalColor};">Countdown for ${username}</div>
                        </div>
                    `;
                    pond.appendChild(duckWrap);

                    let timeLeft = duration;
                    const container = duckWrap.querySelector('.bubble-container');

                    const updateBubble = () => {
                        container.innerHTML = '';
                        const bubbleEl = document.createElement('div');
                        bubbleEl.className = 'speech-bubble active';
                        bubbleEl.innerHTML = timeLeft;
                        container.appendChild(bubbleEl);
                    };

                    updateBubble();

                    const interval = setInterval(() => {
                        timeLeft--;
                        if (timeLeft <= 0) {
                            clearInterval(interval);
                            duckWrap.remove();
                        } else {
                            updateBubble();
                        }
                    }, 1000);
                }
                return;
            }
"""

content = re.sub(
    r'(if \(textTrim === \'!scatter\'\) \{)',
    countdown_cmd.lstrip() + r'\n            \1',
    content
)


with open('index.html', 'w') as f:
    f.write(content)
