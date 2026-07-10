import re

with open('index.html', 'r') as f:
    content = f.read()

# Helper for the new unlurk logic (refreshing image using case-insensitive onerror logic)
refresh_duck_html = r"""`<img src="custom_ducks/${username}.png" alt="${username}" style="width: 100%; height: 100%; object-fit: contain;" onerror="this.onerror = () => { this.onerror = null; this.parentElement.innerHTML = getDuckSVG('${user.duckColor}'); }; this.src = 'custom_ducks/' + '${username}'.toLowerCase() + '.png';" />`"""

# 1. Update lurk command block to add .lurking class
content = re.sub(
    r'(if \(textTrim === \'!lurk\' \|\| text\.includes\(\'karenc9Lurkyduck\'\)\) \{.*?user\.element\.style\.left = Math\.random\(\) > 0\.5 \? \'5%\' : \'95%\';)',
    r'\1\n                user.element.classList.add("lurking");',
    content,
    flags=re.DOTALL
)

# 2. Update time-based unlurk block
old_unlurk_time = r"""if \(Date\.now\(\) - user\.lurkTime > 300000\) \{
                    user\.isLurking = false;
                    if \(user\.originalImage\) \{
                        user\.element\.querySelector\('\.duck-svg'\)\.innerHTML = user\.originalImage;
                    \}
                    // Scatter handles repositioning later, but reset scale and let it re-animate
                    scatterDucks\(\);"""

new_unlurk_time = f"""if (Date.now() - user.lurkTime > 300000) {{
                    user.isLurking = false;
                    user.element.classList.remove("lurking");
                    user.element.querySelector('.duck-svg').innerHTML = {refresh_duck_html};
                    // Scatter handles repositioning later, but reset scale and let it re-animate
                    scatterDucks();"""

content = re.sub(old_unlurk_time, new_unlurk_time, content)

# 3. Add explicit command unlurk block
unlurk_commands = f"""
            if (['!back', '!unlurk', '!bellyflop', '!makeadramaticentrance'].includes(textTrim)) {{
                if (user) {{
                    user.isLurking = false;
                    user.element.classList.remove("lurking");
                    user.element.querySelector('.duck-svg').innerHTML = {refresh_duck_html};
                    scatterDucks();
                }}
                return;
            }}
"""

content = re.sub(
    r'(let user = activeUsers\.get\(username\);)',
    unlurk_commands + r'\n            \1',
    content
)


with open('index.html', 'w') as f:
    f.write(content)
