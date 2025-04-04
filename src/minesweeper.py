from textual.app import App, ComposeResult
from textual.widgets import *
from frontend.views.board import Board
from frontend.views.header import GameHeader
from frontend.views.footer import GameFooter
from frontend.screens.custom_board import CustomBoard
from frontend.custom_widgets.toggle_button import ToggleButton
from frontend.custom_widgets.select_button import SelectButton
from textual.containers import Center
from frontend.themes import themes
from textual.message import Message
from backend.theme_manager import ThemeManager
from backend.game_settings import SettingsManager
from backend.game_statistics import StatisticsManager
from backend.game_engine import GameEngine
from backend.audio_player import AudioPlayer
from frontend.views.cell import Cell
from textual.events import *
from constants import *
from config import *
from game_events import *

CSS = """
Screen {
    align: center middle;
    overflow-x: auto;
}

.enable-hatch {
    hatch: left $primary 5%;
}

Screen > Tooltip {
    padding: 0;
    padding-left: 1;
    padding-right: 1;
    border: thick transparent;
    text-style: bold;
    background: $primary 30%;
}

Screen > Center {
    width: auto;
    height: auto;
}

#coder-title, #game-title {
    text-style: bold;
    color: $text;
    opacity: 50%;
}

#coder-title-container {
    dock: bottom;
    background: $boost;
}

#game-title-container {
    dock: top;
    background: $boost;
}
"""


class MineSweeper(App):
    """Main Minesweeper application class."""

    DEFAULT_CSS = CSS
    TOOLTIP_DELAY = 0.2

    def __init__(self):
        super().__init__()
        self._init_backend()
        self._init_frontend()

    def _init_backend(self):
        """Initialize backend components."""
        self.settings = SettingsManager(SETTINGS_PATH)
        self.statistics = StatisticsManager(STATISTICS_PATH)
        self.audio_player = AudioPlayer(SOUND_FOLDER)
        self.theme_manager = ThemeManager(themes)
        self.engine = GameEngine(self.settings.game_level)

    def _init_frontend(self):
        """Initialize frontend components."""
        self.game_tile = Label(id="game-title")
        self.header_view = GameHeader()
        self.board_view = Board()
        self.footer_view = GameFooter()
        self.creator_title = Label(id="coder-title")

    def on_mount(self):
        """Called when app is mounted in Textual."""

        self._setup_theme()
        self._setup_game_display()
        self.post_event(ThemeChanged(self.theme_manager.emote, self.engine))

    def _setup_theme(self):
        """Set up game theme and visual elements."""
        self.theme_manager.register_themes(self)

        self.theme_manager.set_theme(self, self.settings.game_theme)

        self.app.screen.add_class("enable-hatch")
        self.creator_title.update("libin-codes")

    def _setup_game_display(self):
        """Set up game display with current settings."""
        game_level = self.settings.game_level
        is_custom_game = self.settings.is_custom_game
        stats = self.statistics[game_level] if not is_custom_game else None
        theme_name = self.theme_manager.theme.name
        chord_setting = Chording(self.settings.chording).name
        sound_setting = self.settings.game_sound

        self.game_tile.update(GAME_TITLE_TEMPLATE.format(*game_level))
        self.header_view.init_view(stats)
        self.board_view.init_view(self.engine.grid, game_level)
        self.footer_view.init_view(
            game_level, is_custom_game, theme_name, chord_setting, sound_setting
        )

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield self.header_view
        yield Center(self.game_tile, id="game-title-container")
        yield Center(self.board_view)
        yield self.footer_view
        yield Center(self.creator_title, id="coder-title-container")

    def post_event(self, message: Message):
        self.board_view.post_message(message)
        self.footer_view.post_message(message)
        self.header_view.post_message(message)

    ########## Handling Game Events ##########

    def handle_first_move(self, cell: Cell):
        self.engine.make_move(cell.coordinates, Move.REVEAL)
        self.post_event(
            GameStateChanged(
                self.statistics,
                self.settings,
                self.engine,
                self.theme_manager,
            )
        )
        self.audio_player.play("big_move")

    def handle_chord_move(self, cell: Cell):
        cells_revealed = self.engine.make_move(cell.coordinates, Move.CHORD)
        if cells_revealed:
            if cells_revealed > 9:
                self.audio_player.play("big_move")
            elif cells_revealed:
                self.audio_player.play("chording")

    def handle_reveal_move(self, cell: Cell):
        cells_revealed = self.engine.make_move(cell.coordinates, Move.REVEAL)
        if cells_revealed:
            if cells_revealed > 9:
                self.audio_player.play("big_move")
            elif cells_revealed:
                self.audio_player.play("tile_revealed")

    def handle_flag_move(self, cell: Cell):
        if self.engine.make_move(cell.coordinates, Move.FLAG):
            self.post_event(CellFlagged(self.engine.remaining_flags))
            self.audio_player.play("flag")

    def handle_game_win(self):
        self.post_event(
            GameStateChanged(
                self.statistics,
                self.settings,
                self.engine,
                self.theme_manager,
            )
        )
        if not self.settings.is_custom_game:
            self.statistics.update(
                self.settings.game_level, True, self.board_view.get_time()
            )
        self.audio_player.play("game_won")

    def handle_game_lost(self):
        self.post_event(
            GameStateChanged(
                self.statistics,
                self.settings,
                self.engine,
                self.theme_manager,
            )
        )
        if not self.settings.is_custom_game:
            self.statistics.update(self.settings.game_level, False)
        self.audio_player.play("game_lost")

    def handle_reset(self):
        if (
            self.engine.moves > 1
            and self.engine.game_state == GameState.IN_PROGRESS
            and not self.settings.is_custom_game
        ):
            self.statistics.update(self.settings.game_level, False)
        self.post_event(
            GameStateChanged(
                self.statistics,
                self.settings,
                self.engine,
                self.theme_manager,
            )
        )
        self.engine.reset()

    def handle_theme_selection(self, theme: str):
        self.audio_player.play("button")
        self.settings.update("game_theme", theme)
        self.theme_manager.set_theme(self, theme)
        self.post_event(ThemeChanged(self.theme_manager.emote, self.engine))

    def handle_standard_level_selection(self, level):
        if (
            self.engine.game_state == GameState.IN_PROGRESS
            and self.engine.moves > 1
            and not self.settings.is_custom_game
        ):
            self.statistics.update(self.settings.game_level, False)
        self.audio_player.play("new_level")
        self.settings.update("is_custom_game", False)
        self.settings.update("game_level", GameLevel[level].value)
        self.game_tile.update(GAME_TITLE_TEMPLATE.format(*self.settings.game_level))
        self.engine.reset(GameLevel[level].value)
        self.post_event(
            GameLevelChanged(
                self.statistics, self.settings, self.engine, self.theme_manager
            )
        )

    def on_cell_interaction(self, message: Cell.Interaction):
        """Handle cell interaction events."""
        match message.event.handler_name:
            case "on_mouse_down":
                self.post_event(
                    CellMouseDown(
                        message.event,
                        message.cell,
                        self.settings.chording,
                        self.theme_manager.emote,
                    )
                )
            case "on_mouse_up":
                self.post_event(
                    CellMouseUp(message.event, message.cell, self.theme_manager.emote)
                )
            ########## Handle cell inputs ##########
            case "on_click":
                if self.engine.game_state == GameState.NOT_STARTED:
                    self.handle_first_move(message.cell)
                    return

                if (
                    message.event.button == self.settings.chording
                    and message.cell.is_revealed
                ):
                    self.handle_chord_move(message.cell)
                elif message.event.button == 1:
                    self.handle_reveal_move(message.cell)
                elif message.event.button == 3:
                    self.handle_flag_move(message.cell)

                if self.engine.game_state == GameState.WON:
                    self.handle_game_win()
                elif self.engine.game_state == GameState.LOST:

                    self.handle_game_lost()

    def on_button_pressed(self, message: Button.Pressed):
        """Handle button press events."""
        match message.button.id:
            # handle user clicking on reset button
            case "reset-button" if self.engine.game_state != GameState.NOT_STARTED:
                self.handle_reset()
            case "custom-board-button":
                self.audio_player.play("button")
                self.post_event(ScreenChanged("custom", self.settings))
                self.app.push_screen(CustomBoard(), self.custom_board_dismiss)

            case "selection-button":
                self.audio_player.play("button")

    def on_toggle_button_pressed(self, message: ToggleButton.Pressed):
        """Handle toggle button press events."""
        initial_sound = "🔊" if self.settings.game_sound else "🔇"
        initial_chord = Chording(self.settings.chording).name

        if message.selection not in [initial_chord, initial_sound]:
            self.audio_player.play("toggle")

        match message.selection:
            case chord if chord in list(Chording.__members__.keys()):
                self.settings.update("chording", Chording[chord].value)
            case "🔊":
                self.settings.update("game_sound", True)
                self.audio_player.disabled = False
            case "🔇":
                self.settings.update("game_sound", False)
                self.audio_player.disabled = True

    def custom_board_dismiss(self, level: Tuple[int, int, int] | None):
        """Handle custom board screen dismissal."""
        if level:
            self.audio_player.play("new_level")
            self.settings.update("is_custom_game", True)
            self.settings.update("game_level", level)
            self.game_tile.update(GAME_TITLE_TEMPLATE.format(*self.settings.game_level))
            self.engine.reset(level)
            self.post_event(
                GameLevelChanged(
                    self.statistics,
                    self.settings,
                    self.engine,
                    self.theme_manager,
                )
            )
        self.post_event(ScreenChanged("default", self.settings))

    def on_select_button_pressed(self, message: SelectButton.Pressed):
        """Handle select button press events."""
        match message.selection:
            case theme if theme in [t.name for t in themes]:
                self.handle_theme_selection(theme)

            case level if level != "CUSTOM":
                self.handle_standard_level_selection(level)

            case "CUSTOM":

                self.post_event(ScreenChanged("custom", self.settings))
                self.app.push_screen(CustomBoard(), self.custom_board_dismiss)


if __name__ == "__main__":
    app = MineSweeper()
    app.run()
