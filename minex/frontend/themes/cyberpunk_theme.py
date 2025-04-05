from minex.constants import GameTheme, ThemeEmote

cyberpunk_theme = GameTheme(
    name="CYBERPUNK",
    primary_tile="#C77DFF",  # Lighter purple with pink undertones
    secondary_tile="#93B3FF",  # Lighter blue-purple (blurple)
    victory_flag_tile="#71F5FF",  # Brighter cyan
    primary_bomb_tile="#FF4DB8",  # Brighter pink
    emote=ThemeEmote(
        idle="🌆", click="🌃", lost="💀", win="🌌", flag="💾", mine="👾", misflag="📱"
    ),
)
