const tags = {
  emotes: {
    '25': ['0-4', '6-10'] // Kappa Kappa
  }
};
const message = "Kappa Kappa";
let parts = [];
let lastEnd = 0;
// tmi.js emotes object format: { 'emote_id': ['start-end', 'start-end'] }
// Need to replace the start-end indices with <img src="https://static-cdn.jtvnw.net/emoticons/v2/emote_id/default/dark/1.0">
let replacements = [];
if (tags.emotes) {
  for (const emoteId in tags.emotes) {
    tags.emotes[emoteId].forEach(pos => {
      const [start, end] = pos.split('-').map(Number);
      replacements.push({ start, end, emoteId });
    });
  }
}
replacements.sort((a, b) => a.start - b.start);
let formatted = "";
for (const r of replacements) {
  formatted += message.substring(lastEnd, r.start);
  formatted += `<img src="https://static-cdn.jtvnw.net/emoticons/v2/${r.emoteId}/default/dark/1.0" class="emote" style="vertical-align: middle; height: 1.5em;" />`;
  lastEnd = r.end + 1;
}
formatted += message.substring(lastEnd);
console.log(formatted);
