from typing import Literal
from textual.widget import Widget
from textual.containers import Horizontal
from textual.widgets import Static,Button
from constants import *
from game_events import *
class GameHeader(Widget):
    DEFAULT_CSS = """
    GameHeader {
        dock: top;
        width: 100%;
        background: $boost;
        color: $foreground;
        height: 1;
        layout:horizontal;
        align:center top;
    }

    #left-header{
        height:auto;
        width:auto;
        dock:left;
    }
    #right-header{
        height:auto;
        width:auto;
        dock:right;

    }
    .header-label-left{
        height:auto;
        width:auto;
        border-right:solid $foreground 20%;
        color:$text;
        padding-right:1;
        padding-left:1;
        opacity: 50%;
     
    }
    .header-label-right{
        height:auto;
        width:auto;
        border-left:solid $foreground 20%;
        color:$text;
        padding-right:1;
        padding-left:1;
        opacity: 50%;
    }

    #stats-container{
        height:1;
        width:100%;
  
    }
    #custom-board-button-container{
        height:auto;
        width:auto;
        layer: above;
        position: absolute;
        dock: right;
    }
    #custom-board-button{
        
        height: 1;
        min-width: 1;
        content-align: center middle;
        border: none;
        background: transparent;
        opacity:50%;
        &:focus {
            border: none;
            text-style: bold;
            background-tint: transparent;
        }
        &:hover {
            background: $boost 600%;
        }
        &.-active {
            border: none;
            background: $boost 1200%;
            tint: transparent;
        }
    }
    """

    def compose(self):
        with Horizontal(id='stats-container'):
            with Horizontal(id="left-header"):
                yield Static(classes="header-label-left", id="win_streak")
                yield Static(classes="header-label-left", id="win_rate")
                yield Static(classes="header-label-left", id="best_time")
            with Horizontal(id="right-header"):
                yield Static(classes="header-label-right", id="games_played")
                yield Static(classes="header-label-right", id="games_won")
                yield Static(classes="header-label-right", id="games_lost")
                
        with Horizontal(id="custom-board-button-container"):
            yield Button('🔃 CHANGE SIZE',id='custom-board-button')

    def init_view(self,stats=None):
        if stats:
            self.update_header('default')
            self.refresh_stats(stats)
        else:
            self.update_header('custom')

    def update_header(self,state:Literal['default','custom','hide']):
        if state == 'default':
            self.app.query_one('#stats-container').visible = True
            self.query_one('#custom-board-button-container').visible = False
            self.query_one('#stats-container').visible = True
        elif state == 'custom':
            self.app.query_one('#stats-container').visible = True
            self.query_one('#custom-board-button-container').visible = True
            self.query_one('#stats-container').visible = False
        elif state == 'hide':
            self.app.query_one('#stats-container').visible = False

    @staticmethod
    def format_time(seconds: int | None) -> str:
        if seconds:
            minutes, sec = divmod(seconds, 60)
            return f"{minutes}m {sec}s" if minutes else f"{sec}s"
        return "--"

    def refresh_stats(self,stats:GameStat):
        stats = stats.__dict__
        stats["best_time"] = self.format_time(stats["best_time"])
        streak = str(stats['longest_win_streak'])
        best_time = self.format_time(stats['previous_time'])
        for label in self.query(Static):
            if label.id == "win_streak":
                label.tooltip ="[dim]LONGEST WINNING STREAK:"+streak
            elif label.id == "best_time":
                label.tooltip ="[dim]PREVIOUS TIME:"+best_time
            label.update(stat_view_template[label.id].format(stats[label.id]))


    def on_game_level_changed(self,message:GameLevelChanged):
        if not message.settings.is_custom_game:
            self.update_header('default')
            self.refresh_stats(message.statistics[message.engine.level])
        elif message.settings.is_custom_game:
            self.update_header('custom')

    def on_game_state_changed(self,message:GameStateChanged):
        if message.engine.game_state != GameState.IN_PROGRESS and not message.settings.is_custom_game:
            self.refresh_stats(message.statistics[message.settings.game_level])



    
