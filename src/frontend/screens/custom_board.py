from textual.containers import Grid
from textual.widgets import Input, Button
from textual.validation import Number
from textual.screen import ModalScreen
from textual import events
from textual.binding import Binding

CSS = """
CustomBoard{
    margin:1;
    height:auto;
    width:auto;
}
#custom_modal {
    grid-size: 3 2;
    align: center middle;
    border:panel  $primary 10%;
    outline-left:thick $primary 10%;
    outline-right:thick $primary 10%;
    outline-bottom:thick $primary 10%;
    padding-top:1;
    border-title-color: $secondary;
    width:38;
    height:9;
    padding-left:1;
    padding-right:1;
    border-title-align: center;
    background: $primary 5%;

    
}
#custom_modal > Input{
    border:solid $primary ;
    background:transparent;
    border-title-align: right;
}

#custom_modal > #input_mines{
    border:solid $secondary;
    background:transparent;
    border-title-align: right;
}

#confirm_button{
    column-span: 3;
    width: 100%;
    height:3;
    border:solid $primary 70%;
    background: transparent;
    text-style:none;
    color:$secondary;

    &:focus {
        text-style:none;
        border:solid $primary;
        color: $primary;
        }
    &.-active {
        background: transparent;
        border:solid $secondary;
        tint: transparent;
        }
    &:hover {
        border:solid $primary;
        color: $primary;
    }
    
}
"""


class CustomBoard(ModalScreen):
    DEFAULT_CSS = CSS
    BINDINGS = [
        Binding(key="escape", action="dismiss", description="Dismiss dialog"),
    ]

    def __init__(self, id=None):
        super().__init__(id=id)
        self.x_input_valid = False
        self.y_input_valid = False

    def compose(self):
        yield Grid(
            Input(
                placeholder="8-42",
                id="input_x",
                type="number",
                classes="custom_input",
                max_length=3,
                validators=[Number(minimum=8, maximum=42)],
            ),
            Input(
                placeholder="8-26",
                id="input_y",
                type="number",
                classes="custom_input",
                max_length=3,
                validators=[Number(minimum=8, maximum=26)],
            ),
            Input(
                id="input_mines",
                type="number",
                max_length=3,
                disabled=True,
                classes="custom_input",
            ),
            Button("CONFIRM", id="confirm_button", disabled=True),
            id="custom_modal",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_button":
            x_input = self.query_one("#input_x", Input)
            y_input = self.query_one("#input_y", Input)
            mines_input = self.query_one("#input_mines", Input)
            self.dismiss(
                (int(x_input.value), int(y_input.value), int(mines_input.value))
            )

    def on_mount(self) -> None:
        # Set focus on the X input when the modal appears.
        self.query_one("#input_x", Input).focus()
        self.query_one("#input_x").border_title = "X"
        self.query_one("#input_y").border_title = "Y"
        self.query_one("#input_mines").border_title = "M"
        self.query_one("#custom_modal").border_title = "CUSTOM SIZE"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.focus_next(".custom_input")

    def enable_mine_input(self):
        x_input = self.query_one("#input_x", Input)
        y_input = self.query_one("#input_y", Input)
        mines_input = self.query_one("#input_mines", Input)
        x, y = int(x_input.value), int(y_input.value)
        min_mines = max(1, round(x * y * 0.10))
        max_mines = max(1, round(x * y * 0.70))
        mines_input.validators = [Number(min_mines, max_mines)]
        mines_input.placeholder = f"{min_mines}-{max_mines}"
        if mines_input.disabled:
            mines_input.value = str(max(1, round(x * y * 0.15)))
        mines_input.disabled = False

    def disable_mine_input(self):
        mines_input = self.query_one("#input_mines", Input)
        if mines_input.value:
            mines_input.value = ""
        if mines_input.validators:
            mines_input.validators = []
        if mines_input.placeholder:
            mines_input.placeholder = ""
        mines_input.disabled = True

    def on_input_changed(self, event: Input.Changed) -> None:
        mines_input = self.query_one("#input_mines", Input)
       
        if event.input.id == "input_x":
            if event.validation_result.is_valid:
                self.x_input_valid = True
            else:
                self.x_input_valid = False
                self.disable_mine_input()
        elif event.input.id == "input_y":
            if event.validation_result.is_valid:
                self.y_input_valid = True
            else:
                self.y_input_valid = False
                mines_input.disabled = True
                self.disable_mine_input()
        elif event.input.id == "input_mines":
            if event.validation_result.is_valid:
                self.query_one("#confirm_button").disabled = False
            else:
                self.query_one("#confirm_button").disabled = True
        if self.x_input_valid and self.y_input_valid:
            self.enable_mine_input()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_button":
            x_input = int(self.query_one("#input_x", Input).value)
            y_input = int(self.query_one("#input_y", Input).value)
            mines_input = int(self.query_one("#input_mines", Input).value)
            level = (x_input, y_input, mines_input)
            self.dismiss(level)

    def action_dismiss(self) -> None:

        self.dismiss()

    def on_click(self, event: events.Click) -> None:
        if event.widget.__class__ not in [Grid, Input, Button]:
            self.dismiss()
