import re

with open("index.html", "r") as f:
    content = f.read()

# Only change imgBg.src
content = content.replace("imgBg.src = `assets/pond_backgrounds/${encodeURIComponent(POND_BACKGROUND)}`;", "imgBg.src = `assets/pond_backgrounds/${encodeURIComponent(POND_BACKGROUND)}?v=${Date.now()}`;")

with open("index.html", "w") as f:
    f.write(content)
