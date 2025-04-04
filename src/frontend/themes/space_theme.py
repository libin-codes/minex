from constants import GameTheme,ThemeEmote

space_theme = GameTheme(
    name="SPACE",
    primary_tile="#7575A3" ,
    secondary_tile="#A7B4D0",
    victory_flag_tile="#f3826f",
    primary_bomb_tile="#ffce00",
    emote=ThemeEmote(
        idle="🚀",
        click="🛸",
        mine='👽',
        flag='🚩',
        lost='💥',
        win='🪐',
        misflag='🌑'
    )
)
