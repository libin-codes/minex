from textual.widget import Widget
from textual.widgets import Button
from textual.message import Message 
from textual.reactive import reactive

CSS = '''
ToggleButton{
    height:auto;
    width:auto;
}

#toggle-button {
    height: 1;
    width:auto;
    min-width: 1;
    border: none;
    background: transparent;
    text-style:bold;
    &:focus {
        border: none;
        text-style: bold;
        background-tint: transparent;
    }
    &:hover {
        background: $boost;
    }
    &.-active {
        border: none;
        background: $boost 300%;
        tint: transparent;
    }
}



'''


class ToggleButton(Widget):
    DEFAULT_CSS = CSS
    class Pressed(Message):
        def __init__(self,selection: str) -> None:
            super().__init__()
            self.selection = selection
    
    selection = reactive(None,init=False)   
    selection_list = reactive(None,init=False)
  
        
    def compose(self):
        yield Button(id='toggle-button')

    def watch_selection(self,old_value,new_value):
        button = self.query_one(Button)
        if not old_value:
            max_length = len(max(self.selection_list, key=len))
            button.styles.width = max_length + 3

        button.label = new_value
        self.post_message(self.Pressed(new_value))

    def on_button_pressed(self):
        self.selection = self.selection_list[
            (self.selection_list.index(self.selection) + 1) % 
            len(self.selection_list)
            ]
