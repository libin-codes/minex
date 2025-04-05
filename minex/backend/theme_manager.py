from dataclasses import dataclass
from typing import List
from textual.theme import Theme
from textual.app import App
from minex.constants import GameTheme

class ThemeManager:
    theme = None
    emote = None
    def __init__(self,themes:List[GameTheme]):
        self.themes = themes

    def register_themes(self,app:App):
        for theme in self.themes:
            theme = Theme(
                name=theme.name,
                primary=theme.primary_tile,
                secondary=theme.secondary_tile,
                error = theme.primary_bomb_tile,
                success=theme.victory_flag_tile,
                )
            app.register_theme(theme)

    def set_theme(self,app:App,theme_name:str):
        for theme in self.themes:
            if theme.name == theme_name:
                app.theme = theme.name
                self.theme = theme
                self.emote = theme.emote
                break
  
          


    

 