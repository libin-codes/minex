from minex.constants import GameTheme,ThemeEmote

winter_theme = GameTheme(
    name="WINTER",
    primary_tile="mediumturquoise",    # Ice blue
    secondary_tile="aliceblue",        # Soft snow color
    victory_flag_tile="powderblue",    # Victory blue
    primary_bomb_tile="steelblue",     # Deep winter blue
    emote=ThemeEmote(
        idle="⛄",     # Snowman
        click="⛄",  
        lost="🥶",     # Melting snowman
        win="🏂",      # Snow activity
        flag="🚩",     # Ice cube
        mine="🐻",  
        misflag="🐇"   # Snow cloud
    )
)
