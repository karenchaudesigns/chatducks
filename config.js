const CONFIG = {
    POND_BACKGROUND: "", // Filename in assets/pond_backgrounds/ or null/empty for default SVG
    INACTIVITY_LIMIT_MS: 60000 * 30, // 30 minutes. Ducks leave if silent this long.
    BUBBLE_DURATION_MS: 150000       // 5 minutes. How long chat bubbles stay up.
,
    // Streamer.bot WebSocket Integration
    ENABLE_STREAMER_BOT: true,
    STREAMER_BOT_WS_URL: 'ws://127.0.0.1:8080/',
    STREAMER_BOT_REWARD_ACTIONS: {
        // Map reward names (exact, case-insensitive) to overlay commands
        // Example: "Pond Treats": "!treats",
        // Example: "Confetti Party": "!yay",
        "duck treats": "!treats",
        "scatter ducks": "!scatter",
        "clear pond": "!shoo"
    }
};
