from textual.widgets import ListView, ListItem, Label
from textual.screen import ModalScreen
from textual import events

class OptionOverlay(ModalScreen):
  
    SCOPED_CSS = False
    DEFAULT_CSS = """

    OptionOverlay > ListView {
        position: absolute;
        height:auto;
        width:auto;

    }
    OptionOverlay > Label {
        position: absolute;
        text-style: bold not dim;
        background: $primary 10%;
        content-align: center middle;
    }
    ListItem {
        padding-left: 1;
        &.-highlight {
                color: $background !important;
                background: $primary !important;
                text-style: bold !important;
             
                
            }
    }

    """
    

    def __init__(self, options: list[str], index, anchor) -> None:
        super().__init__()
        self.options = options
        self.anchor = anchor
        self.index = index

    def compose(self):
        yield Label('SELECT', id="select-label")
        yield ListView(
            *[ListItem(Label(opt)) for opt in self.options], initial_index=self.index
        )
        
    def on_mount(self) -> None:
        anchor_region = self.anchor.region
        select_label = self.query_one(Label)
        select_label.styles.width = len(max(self.options, key=len)) + 3
        list_view = self.query_one(ListView)
        list_view.styles.width = anchor_region.width
        vertical_offset = anchor_region.y - len(self.options)
        list_view.styles.offset = (anchor_region.x, vertical_offset)
        select_label.styles.offset = (anchor_region.x, vertical_offset +len(self.options))
     

    def on_list_view_selected(self, event: events.Event) -> None:
        selected_index = self.query_one(ListView).index
    
        self.dismiss(self.options[selected_index])

    def on_click(self, event: events.Click) -> None:
        if event.widget.__class__ != ListView:
            self.dismiss(self.options[self.query_one(ListView).index])
