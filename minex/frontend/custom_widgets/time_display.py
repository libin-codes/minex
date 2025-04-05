from time import monotonic
from textual.reactive import reactive
from textual.widgets import Static

class TimeDisplay(Static):
    """A widget to display elapsed time."""

    start_time = reactive(monotonic)
    time = reactive(0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1, self._update_time, pause=True)

    def _update_time(self) -> None:
        """Method to update the time to the current time."""
        self.time = monotonic() - self.start_time

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        self.update(str(int(time)))

    ##### methods to use #########

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self):
        """Method to stop the time display updating."""
        self.update_timer.pause()

    def resume(self,time=None):
        self.start_time = monotonic() - (time if time else self.time)
        self.update_timer.resume()


    def reset(self):
        """Method to reset the time display to zero."""
        self.update_timer.pause()
        self.start_time = monotonic()
        self.time = 0


