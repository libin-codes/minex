from constants import GameTheme,ThemeEmote


desert_theme = GameTheme(
    name="DESERT",
    primary_tile="#D79E54",
    secondary_tile="#94C5CC",
    victory_flag_tile="#7EB77F",
    primary_bomb_tile="#B22222",

    emote=ThemeEmote(
        idle="🌵",
        click="🌅",
        lost="💀",
        win="🌴",
        flag="🚩",
        mine="🐍",  
        misflag="❌"
    )
)








'''Primary: "#D79E54"  // Sandy gold
Secondary: "#94C5CC" // Oasis blue
Panel: "#8B5D33"    // Dark sand
Emojis: 🌵 (idle), 🏜️ (click), 💀 (lost), 🌴 (win), 🧭 (flag), 🦂 (mine), ❌ (misflag)
'''