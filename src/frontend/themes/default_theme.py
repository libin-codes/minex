from constants import GameTheme,ThemeEmote

default_theme = GameTheme(
    name="DEFAULT",
    primary_tile="palegreen",
    secondary_tile="beige",
    victory_flag_tile="gold",
    primary_bomb_tile="red",
    emote=ThemeEmote(
        idle  ="🙂",
        click ="😮",
        lost  ="😵",
        win   ="😎",
        flag  ="🚩",
        mine  ="💣",
        misflag ="❌"
    )
)