import re

with open('index.html', 'r') as f:
    content = f.read()

# Add a CSS class for conversing state to freeze animation and allow explicit scaleX control
conversing_css = """
        .conversing .duck-swim, .conversing .duck-svg {
            animation: none !important;
        }
        .conversing.facing-left .duck-svg {
            transform: scaleX(-1) !important;
        }
        .conversing.facing-right .duck-svg {
            transform: scaleX(1) !important;
        }
"""
content = re.sub(
    r'(/\* === SPEECH BUBBLES === \*/)',
    conversing_css + r'\n        \1',
    content
)

# Add logic in handleIncomingMessage
# We place this after `user` has been spawned/updated, and before rendering the speech bubble.
reply_logic = r"""
            // REPLY LOGIC
            if (tags && tags['reply-parent-user-login']) {
                const parentUsername = tags['reply-parent-user-login'];
                // Check if parent user is case-insensitively active. tmi.js tags are usually lowercase, but let's be safe.
                let parentUser = activeUsers.get(parentUsername);
                if (!parentUser) {
                    for (let [key, val] of activeUsers.entries()) {
                        if (key.toLowerCase() === parentUsername.toLowerCase()) {
                            parentUser = val;
                            break;
                        }
                    }
                }

                if (parentUser && !parentUser.isLurking && !parentUser.isStatic && !user.isStatic) {
                    // Calculate meeting point
                    const meetingPoint = Math.random() * 60 + 20; // Between 20% and 80%

                    user.element.classList.add('conversing');
                    parentUser.element.classList.add('conversing');

                    // User A replies to User B. User B (parent) swims up to User A (user).
                    // They face each other.
                    // Let User A be on the left (meetingPoint - 5), User B on the right (meetingPoint + 5)
                    user.element.style.left = `${meetingPoint - 5}%`;
                    parentUser.element.style.left = `${meetingPoint + 5}%`;

                    user.element.classList.remove('facing-left');
                    user.element.classList.add('facing-right');

                    parentUser.element.classList.remove('facing-right');
                    parentUser.element.classList.add('facing-left');

                    setTimeout(() => {
                        user.element.classList.remove('conversing', 'facing-right', 'facing-left');
                        parentUser.element.classList.remove('conversing', 'facing-right', 'facing-left');
                        scatterDucks();
                    }, 15000); // Talk for 15 seconds then scatter
                }
            }
"""

content = re.sub(
    r'(// 3\. Display the chat message)',
    reply_logic.lstrip() + r'\n            \1',
    content
)


with open('index.html', 'w') as f:
    f.write(content)
