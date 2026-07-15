# Twitch Duck Overlay

A fun, interactive chat overlay for Twitch that spawns a swimming duck for each active chatter in your stream. Messages appear as speech bubbles, and specific actions trigger unique behaviors!

## Setup Instructions for OBS / Streamlabs
1. Add a **Browser Source** to your scene.
2. Set the URL to your hosted `index.html` file, and append your channel name as a parameter:
   `https://your-url.com/index.html?channel=YOUR_NAME`
3. Set the dimensions (e.g., 1920x1080) to cover your screen or specific area.
4. Check "Allow background transparency".

## Custom Ducks
You can give users specific custom ducks (instead of the dynamically generated colored SVGs).
Place a `.png` file inside the `assets/custom_ducks/` folder matching their Twitch username. The system is case-insensitive, so both `TechJeeper.png` and `techjeeper.png` will work.

## Commands

### User Commands
- `!lurk`: Puts the user in "lurk mode" - they turn into a Lurkyduck and chill in the back corner of the pond.
- `!unlurk` / `!back` / `!bellyflop` / `!makeadramaticentrance`: Removes lurk mode, refreshes their custom duck image, and makes them swim normally again. (Talking within 5 minutes of a !lurk command also triggers this).
- `!countdown <duration>`: Spawns a dedicated duck in the corner with a chat bubble that ticks down for the specified duration (in seconds).

### Mod/Broadcaster Commands
- `!shoo` / `!reset`: Instantly clears the pond of all ducks and countdowns.
- `!clear`: Clears all current chat bubbles and action text without removing the ducks.
- `!scatter`: Forces all active ducks to randomly reposition themselves horizontally along the pond.

## Features
- **Replies**: When one user replies to another in Twitch chat, their ducks will temporarily swim up to each other and converse face-to-face.
- **Directional Swimming**: Ducks now intelligently face the direction they are actively swimming.
- **Emote Support**: Fully parses and displays standard Twitch emotes inside speech bubbles and action text!
