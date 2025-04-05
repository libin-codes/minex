from textual.widget import Widget
from textual.widgets import Button
from textual.message import Message
from ..screens.option_overlay import OptionOverlay
from textual.reactive import reactive


CSS = '''
SelectButton {
    height: auto;
    width: auto;
    
}
#selection-button {
    height: 1;
    min-width: 1;
    content-align: center middle;
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





class SelectButton(Widget):
    class Pressed(Message):
        def __init__(self,id, selection: str) -> None:
            super().__init__()
            self.selection = selection
            self.id = id
    DEFAULT_CSS = CSS
    selection = reactive(None,init=False)
    options = reactive(None,init=False)
    colors = reactive(None,init=False)

    def compose(self):
        yield Button(id="selection-button")

    

    def watch_selection(self,old_value,new_value):
        button = self.query_one(Button)
        button.label = new_value
        button.styles.color = self.colors[self.options.index(new_value)] if self.colors else ''
        if old_value and new_value != old_value:
            self.post_message(self.Pressed(self.id,self.selection))
        else:
            max_length = len(max(self.options, key=len))
            button.styles.width = max_length + 3
    
    def on_button_pressed(self):  
        self.app.push_screen(
            OptionOverlay(
                self.options, self.options.index(self.selection), self
                ), 
            lambda selection: setattr(self, 'selection', selection)
        )

    def set_options(self,options,colors=None):
        self.colors = colors
        self.options = options