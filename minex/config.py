from pathlib import Path
import os

STATISTICS_PATH = Path.home() / ".minesweeper-tui" / "statistics.bin"
SETTINGS_PATH = Path.home() / ".minesweeper-tui" / "settings.bin"
SOUND_FOLDER = Path(os.path.dirname(__file__)) / "sounds"

