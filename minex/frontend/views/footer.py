from textual.widget import Widget
from textual.widgets import Label
from minex.backend.game_settings import SettingsManager
from minex.frontend.custom_widgets.select_button import SelectButton
from minex.frontend.custom_widgets.toggle_button import ToggleButton
from minex.constants import GameLevel
from minex.frontend.themes import themes
from minex.constants import Chording
from minex.game_events import ScreenChanged
from textual.containers import Horizontal

class GameFooter(Widget):
    DEFAULT_CSS = """
    GameFooter {
        height:1;
        width: 100%;
        background: $boost;
        color: $foreground;
        dock:bottom;
        layout:horizontal;
        align:center middle;
    }
    #select-button-container{
        width:auto;
        height:auto;
        dock:left;
    }
    #toggle-button-container{
        width:auto;
        height:auto;
        dock:right;
    }
    #creator-title{
        offset:-1 0;
        text-style: bold;
        color: $text;
        opacity: 50%;
    }
        
    """

    def compose(self):
        with Horizontal(id='select-button-container'):
            yield SelectButton(id='mode-button')
            yield SelectButton(id='theme-button')
        with Horizontal(id='toggle-button-container'):
            yield ToggleButton(id='chord-button')
            yield ToggleButton(id='sound-button')

        yield Label('libin-codes',id='creator-title')

    def init_mode_button(self,game_level,is_custom_game):
        mode_button = self.query_one('#mode-button',SelectButton)
        if is_custom_game:
            initial_game_mode = 'CUSTOM'
        else:
            initial_game_mode = GameLevel(game_level).name

        mode_button.options = ["CUSTOM"]+[mode.name for mode in GameLevel][::-1]
        mode_button.selection = initial_game_mode

    def init_theme_button(self,theme_name):
        theme_button = self.query_one('#theme-button',SelectButton)
        game_themes = [theme.name for theme in themes][::-1]
        theme_colors = [theme.primary_tile for theme in themes][::-1]
    
        theme_button.colors = theme_colors
        theme_button.options = game_themes
        theme_button.selection = theme_name

    def init_chord_button(self,chord_setting):
        chord_button = self.query_one('#chord-button',ToggleButton)
        chord_button.selection_list = [chord.name for chord in Chording]
        chord_button.selection = chord_setting
    
    def init_sound_button(self,sound_setting):
        sound_button = self.query_one('#sound-button',ToggleButton)
        sound_button.selection_list = ["🔊","🔇"]
        sound_button.selection = '🔊' if sound_setting else '🔇'
     
    def init_view(self,settings:SettingsManager,theme_name:str):
        self.init_mode_button(settings.game_level,settings.is_custom_game)
        self.init_theme_button(theme_name)
        self.init_chord_button(Chording(settings.chording).name)
        self.init_sound_button(settings.game_sound)


    def on_screen_changed(self,message:ScreenChanged):
        if message.screen == 'default' and not message.settings.is_custom_game:  
            level_name = GameLevel(message.settings.game_level).name
            self.query_one('#mode-button',SelectButton).selection = level_name

        elif message.screen == 'custom' and not message.settings.is_custom_game:
            mode_button = self.query_one('#mode-button',SelectButton)
            mode_button.query_one("Button").label = GameLevel(message.settings.game_level).name

        elif message.screen == 'default' and message.settings.is_custom_game:
            mode_button = self.query_one('#mode-button',SelectButton)
            mode_button.query_one("Button").label = "CUSTOM"
            
            

  