import pickle
from typing import Optional, Tuple, Union
from pathlib import Path
from minex.constants import GameLevel, GameStat, Statistics

class StatisticsManager:
    """Manager for game statistics across different levels."""
    def __init__(self, statistics_path: Path):
        self.statistics_path = statistics_path

    def _get_statistics(self) -> Statistics:
        try:
            with open(self.statistics_path, "rb") as f:
                data = pickle.load(f)
                # depends on the game level
                if isinstance(data, dict) and GameLevel.values() == list(data.keys()):
                    return data
                raise Exception("Statistics file is corrupted")
        except Exception:
            self._save_stats({level.value: GameStat() for level in GameLevel})
            return self._get_statistics()

    def _save_stats(self, stats: Statistics) -> None:
        self.statistics_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.statistics_path, "wb") as f:
            pickle.dump(stats, f)

    def __getitem__(self, key: Union[GameLevel, Tuple[int, int, int]]) -> GameStat:
        if isinstance(key, GameLevel):
            return self._get_statistics()[key.value]
        return self._get_statistics()[key]
    

    def update(
        self,
        level: Tuple[int, int, int],
        result: bool,
        time: Optional[int] = None,
    ):
        stats = self._get_statistics()
        stats[level].games_played += 1
        if result:  # Game won
            stats[level].games_won += 1
            stats[level].win_streak += 1
            if (
                stats[level].win_streak
                > stats[level].longest_win_streak
            ):
                stats[level].longest_win_streak = stats[level].win_streak
            if time is not None:
                stats[level].previous_time = time
                if (
                    stats[level].best_time is None
                    or time < stats[level].best_time
                ):
                    stats[level].best_time = time
        else:  # Game lost
            stats[level].games_lost += 1
            stats[level].win_streak = 0  # Reset win streak on loss

        if stats[level].games_played > 0:
            stats[level].win_rate = round(
                (stats[level].games_won / stats[level].games_played)
                * 100,
                2,
            )
        self._save_stats(stats)

