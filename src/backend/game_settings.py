from pathlib import Path
import pickle
from typing import Any, Literal
from frontend.themes import themes
from constants import GameLevel, Chording

class SettingsManager():
    game_level: GameLevel = GameLevel.EASY.value
    chording: Chording = Chording.LEFT_CLICK
    game_sound: bool = True
    game_theme: str = themes[0].name
    is_custom_game: bool = False
    def __init__(self, settings_path: Path):
        self.settings_path = settings_path
        self._init_settings()

    def _init_settings(self):
        try:
            with open(self.settings_path, "rb") as f:
                data = pickle.load(f)
                if not isinstance(data,self.__class__):
                    raise Exception("Settings file is corrupted")
                self.game_level = data.game_level
                self.chording = data.chording
                self.game_sound = data.game_sound
                self.game_theme = data.game_theme
                self.is_custom_game = data.is_custom_game
        except Exception:
            self._save_settings()

    def _save_settings(self):
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.settings_path, "wb") as f:
            pickle.dump(self, f)

    def update(self,setting: Literal['game_level','chording','game_sound','game_theme','is_custom_game'],value: Any):
        setattr(self, setting, value)
        self._save_settings()

