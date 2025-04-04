from textual.message import Message
from backend.theme_manager import ThemeManager
from constants import COORDINATE, GameState, ThemeEmote, Chording
from backend.game_statistics import Statistics
from backend.game_settings import SettingsManager
from backend.game_engine import GameEngine
from typing import Literal
from textual.events import MouseDown, MouseUp

class CellFlagged(Message):
    """Message sent when a cell is flagged."""
    def __init__(self, flag_count: int):
        self.flag_count = flag_count
        super().__init__()

class GameStateChanged(Message):
    """Message sent when the game state changes."""

    def __init__(self,statistics:Statistics,settings:SettingsManager,engine:GameEngine,theme_manager:ThemeManager):
        self.statistics = statistics
        self.settings = settings
        self.engine = engine
        self.theme_manager = theme_manager
        super().__init__()


class GameLevelChanged(Message):
    """Message sent when the game level changes."""

    def __init__(
        self,
        statistics: Statistics,
        settings: SettingsManager,
        engine: GameEngine,
        theme_manager: ThemeManager,
    ):
        self.statistics = statistics
        self.settings = settings
        self.engine = engine
        self.theme_manager = theme_manager
        super().__init__()

class ScreenChanged(Message):
    """Message sent when the screen changes."""

    def __init__(self, screen:Literal['default','custom'],settings:SettingsManager):
        self.screen = screen
        self.settings = settings
        super().__init__()


class ThemeChanged(Message):
    """Message sent when the theme changes."""

    def __init__(self, theme_emote:ThemeEmote,engine:GameEngine):
        self.emote = theme_emote
        self.engine = engine
        super().__init__()

class CellMouseDown(Message):
    """Message sent when the mouse is down on a cell."""

    def __init__(self,event:MouseDown,cell,chording:Chording,emote:ThemeEmote):
        self.cell = cell
        self.event = event
        self.chording = chording
        self.emote = emote
        super().__init__()

class CellMouseUp(Message):
    """Message sent when the mouse is up on a cell."""

    def __init__(self,event:MouseUp,cell,emote:ThemeEmote):
        self.cell = cell
        self.event = event
        self.emote = emote
        super().__init__()


