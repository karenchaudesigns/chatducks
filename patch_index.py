import re

with open("index.html", "r") as f:
    content = f.read()

# Instead of my buggy find_matching_brace, use a simpler regex replacement approach.
# Let's count handleStreamStreak manually and replace using replace_with_git_merge_diff conceptually

# We know exactly where the lines are. Let's read by lines.
with open("index.html", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    # duplicate handleStreamStreak starts at 1701
    if i == 1700 and "async function handleStreamStreak" in line:
        skip = True

    if skip and i == 1805 and "user.isBusy = false;" in line:
        pass
    if skip and i == 1806 and "}" in line:
        skip = False
        continue

    if not skip:
        new_lines.append(line)

lines = new_lines
new_lines = []
for line in lines:
    if "async function handleStreamStreak(username, count, tags) {" in line:
        new_lines.append(line)
        new_lines.append("            const streakSpeed = (typeof CONFIG !== 'undefined' && CONFIG.STREAK_SPEED_MS) ? CONFIG.STREAK_SPEED_MS : 4000;\n")
    elif "await new Promise(resolve => setTimeout(resolve, 2000));" in line:
        new_lines.append(line.replace("2000", "streakSpeed"))
    elif "user.element.style.transition = 'left 2s linear';" in line:
        new_lines.append(line.replace("'left 2s linear'", "`left ${streakSpeed / 1000}s linear`"))
    else:
        new_lines.append(line)

with open("index.html", "w") as f:
    f.writelines(new_lines)
