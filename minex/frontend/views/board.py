from textual.widgets import Button
from textual.containers import Horizontal, Grid
from textual.widget import Widget
from textual.reactive import reactive
from textual.widgets import Static
from minex.frontend.custom_widgets.time_display import TimeDisplay
from minex.frontend.views.cell import Cell
from minex.game_events import *
from minex.constants import GameState


from typing import Literal

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]



CSS = """
Board{
    margin:1;
    width:auto;
    height:auto;
}
#grid{
    border-left:tall transparent;
    border-right:tall transparent;
}

#header-container{
    layout:horizontal;
    height:3;
    width:100%;
    align:center middle;
    border-left:thick transparent;
    border-right:thick transparent;
    background:$primary 10%;
    padding-left:1;
 
 
}
.panel{
    width:5;
    height:1;
    text-style: bold dim;
    margin-top:1;
    margin:1;

    
}

#time-display{
    content-align:left middle;
}

#flag-display{
    content-align:right middle;
}


#reset-button{
    height:3;
    min-width:5;
    align:center middle;
    
    content-align:center middle;
    border-top:thick transparent;
    border-bottom:thick transparent;
    background:transparent;
    &:focus {
        text-style: bold;
        background-tint: transparent;
    }
    &:hover{
        background:$boost;
    }
    &.-active{
        border:none;
        background:$boost 300%;
        tint: transparent;
        border-top:thick transparent;
        border-bottom:thick transparent;
    }
}
"""


class Board(Widget):
    DEFAULT_CSS = CSS
    SCOPED_CSS = True

    flag_display = reactive(0, init=False)

    def compose(self):
        with Horizontal(id="header-container"):
            yield Static(classes="panel", id="flag-display")
            yield Button(id="reset-button")
            yield TimeDisplay(classes="panel", id="time-display")
        yield Grid(id="grid")

    def watch_flag_display(self, value):
        self.query_one("#flag-display", Static).update(str(value))

    ######### helper methods ##########

    def update_emote(self, emote):
        self.query_one("#reset-button", Button).label = emote

    def mount_grid(self, grid, level):
      
        view_grid = self.query_one(Grid)
        view_grid.remove_children()
        view_grid.mount_all([cell for row in grid[::-1] for cell in row])
        view_grid.styles.width = (level[0] * 3) + 2
        view_grid.styles.height = level[1]
        view_grid.styles.grid_size_rows = level[1]
        view_grid.styles.grid_size_columns = level[0]

    def init_view(self, grid, level):
        
        self.mount_grid(grid, level)
        self.flag_display = level[-1]


    def reset(self, engine:GameEngine, emote):
        self.update_emote(emote)
        self.flag_display = engine.level[-1]
        cells = [cell for row in engine.grid for cell in row]
        for cell in cells:
            cell.reset()
    
    def update_timer(
        self,
        state: Literal["start", "stop", "restart"],
    ):
        time_display = self.query_one("#time-display", TimeDisplay)
        if state == "start":
            time_display.start()
        elif state == "stop":
            time_display.stop()
        elif state == "restart":
            time_display.reset()

    def get_time(self):
        return int(self.query_one("#time-display", TimeDisplay).time)

    ########## event handlers ##########
    def on_cell_flagged(self,message:CellFlagged):
        self.flag_display = message.flag_count

    def on_game_state_changed(self,message:GameStateChanged):
        # handle game start
        cells = [cell for row in message.engine.grid for cell in row]
        if message.engine.moves == 1:
            self.update_timer("start")
        # handle game win
        if message.engine.game_state == GameState.WON:
            self.update_timer("stop")
            for cell in cells:
                if cell.content == -1 and cell.is_flagged:
                    cell.classes = ["victory_flag_tile"]
                    cell.set_tile("victory")
                cell.disabled = True
            self.update_emote(message.theme_manager.emote.win)
        # handle game loss
        elif message.engine.game_state == GameState.LOST:
            self.update_timer("stop")
            for cell in cells:
                cell.disabled = True
                if cell.content == -1 and not cell.is_flagged:
                    if cell.is_revealed:
                        cell.set_tile("loss")
                    cell.update(message.theme_manager.emote.mine)
                elif cell.content != -1 and cell.is_flagged:
                    cell.update(message.theme_manager.emote.misflag)
            self.update_emote(message.theme_manager.emote.lost)

        # handle game reset
        if message.engine.moves == 0:
            self.reset(message.engine, message.theme_manager.emote.idle)
            self.update_timer("restart")


    def on_game_level_changed(self,message:GameLevelChanged): 
        self.update_timer("restart")
        self.flag_display = message.engine.level[-1]
        self.update_emote(message.theme_manager.emote.idle)
        self.mount_grid(message.engine.grid, message.engine.level)


    def on_screen_changed(self,message:ScreenChanged):
        if message.screen == "default":
            self.display = "block"
        elif message.screen == "custom":
            self.display = "none"


    def on_theme_changed(self,message:ThemeChanged):
        Cell.flag_emote = message.emote.flag
        for cell in [cell for row in message.engine.grid for cell in row]:
            if cell.is_flagged:
                cell.update(Cell.flag_emote)
   
        if message.engine.game_state in [GameState.IN_PROGRESS,GameState.NOT_STARTED]:
            self.update_emote(message.emote.idle)
        elif message.engine.game_state == GameState.WON:
            self.update_emote(message.emote.win)
        elif message.engine.game_state == GameState.LOST:
            self.update_emote(message.emote.lost)
            for cell in [cell for row in message.engine.grid for cell in row]:
                if cell.content == -1:
                    cell.update(message.emote.mine)
                if cell.content != -1 and cell.is_flagged:              
                    cell.update(message.emote.misflag)
        
        
    def on_cell_mouse_down(self,message:CellMouseDown):
        self.update_emote(message.emote.click)
        
    def on_cell_mouse_up(self,message:CellMouseUp):
        self.update_emote(message.emote.idle)



        
               
