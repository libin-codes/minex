from typing import Union
from textual.widgets import Static
from textual.reactive import reactive
from textual.events import MouseDown, MouseUp, Click
from minex.constants import *
from textual.message import Message


CSS = """
Cell{
    width:3;
    height:3;
    content-align:center middle;
    text-style: bold; 
    
    &.hide_tile{
        background:$primary;
        &:hover{
            background:$primary-darken-3;
        }
    }
    &.reveal_tile{
        background:$secondary;
        &:hover{
            background:$secondary-darken-3;
        }
    }
    &.bomb_tile{
        background:$error;
    }

    &.flag_tile{
        background:$success;
    }

}

"""


class Cell(Static):
    class Interaction(Message):
        def __init__(self, cell, event:Union[ MouseDown , MouseUp , Click]):
            super().__init__()
            self.cell = cell
            self.event = event

    DEFAULT_CSS = CSS

    is_flagged = reactive(False, init=False)
    is_revealed = reactive(False, init=False)
    flag_emote = None

    def __init__(self, coordinates, classes=None) -> None:
        super().__init__(content=" ", classes=classes)
        self.content = 0
        self.coordinates = coordinates
        self.set_tile("hidden")

    def on_mount(self):

        if sum(self.coordinates) % 2 == 0:
            self.styles.opacity = 0.98

    ############### watching reactive attributes ###############
    def watch_is_revealed(self):
        if self.is_revealed and self.content != -1:
            self.set_tile("revealed")
            self.styles.color = DIGIT_COLOR[self.content]
            self.update(str(self.content) if self.content != 0 else " ")
            if self.content == 0:
                self.disabled = True

    def watch_is_flagged(self, prevoius_value, new_value):
        self.update(self.flag_emote if self.is_flagged else " ")

    ############### managing mouse inputs ###############

    def on_click(self, event: Click) -> None:
        self.app.post_message(self.Interaction(self, event))

    def on_mouse_down(self, event: MouseDown):
        self.app.post_message(self.Interaction(self, event))

    def on_mouse_up(self, event: MouseUp):
        self.app.post_message(self.Interaction(self, event))

    ############### view management methods ###############

    def reset(self):
        self.content = 0
        self.is_revealed = False
        self.is_flagged = False
        self.set_tile("hidden")
        self.disabled = False
        self.update(" ")

    def set_tile(self, state: TILE_STATE):
        self.classes = {
            "revealed": ["reveal_tile"],
            "hidden": ["hide_tile"],
            "victory": ["flag_tile"],
            "loss": ["bomb_tile"],
        }[state]
