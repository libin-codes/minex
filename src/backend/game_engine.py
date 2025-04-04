from typing import List, Tuple, Set
import random
from constants import GameLevel, GameState, Move, COORDINATE, DIRECTIONS
from frontend.views.cell import Cell


class GameEngine:
    """Game engine for Minesweeper that handles game logic and state."""

    def __init__(self, game_level: Tuple[int, int, int]) -> None:
        """Initialize game engine with given level (width, height, mines)."""
        self.level = game_level
   
        self.grid = [
            [Cell((x, y)) for x in range(game_level[0])] for y in range(game_level[1])
        ]
        self.game_state = GameState.NOT_STARTED
        self.moves = 0
        
        self._revealed_count = 0
        self._mine_locations = set()

    @property
    def remaining_flags(self) -> int:
        """Get number of remaining flags."""
        return self.level[2] - sum(
            1 for row in self.grid for cell in row if cell.is_flagged
        )

    def _get_neighbors(self, x: int, y: int) -> List[COORDINATE]:
        """Get valid neighboring coordinates."""
        return [
            (x + dx, y + dy)
            for dx, dy in DIRECTIONS
            if 0 <= x + dx < self.level[0] and 0 <= y + dy < self.level[1]
        ]

    def _generate_mines(self, first_click: COORDINATE, safe_radius: int = 1) -> None:
        """Generate mines avoiding the first click area."""
        fx, fy = first_click
        while len(self._mine_locations) < self.level[2]:
            x = random.randint(0, self.level[0] - 1)
            y = random.randint(0, self.level[1] - 1)
            if (x, y) not in self._mine_locations and not (
                abs(x - fx) <= safe_radius and abs(y - fy) <= safe_radius
            ):
                self._mine_locations.add((x, y))
                self.grid[y][x].content = -1
        self._calculate_numbers()

    def _calculate_numbers(self) -> None:
        """Calculate numbers for cells adjacent to mines."""
        for x, y in self._mine_locations:
            for nx, ny in self._get_neighbors(x, y):
                cell = self.grid[ny][nx]
                if cell.content != -1:
                    cell.content += 1

    def _flood_fill(self, x: int, y: int) -> None:
        """Reveal empty cells and their neighbors."""
        stack = [(x, y)]
        visited = set()

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited or self.grid[cy][cx].is_flagged:
                continue

            cell = self.grid[cy][cx]
            if not cell.is_revealed:
                cell.is_revealed = True
                self._revealed_count += 1

            visited.add((cx, cy))
            if cell.content == 0:
                stack.extend(
                    (nx, ny)
                    for nx, ny in self._get_neighbors(cx, cy)
                    if (nx, ny) not in visited
                )

    def _handle_first_move(self, x: int, y: int) -> None:
        """Handle the first move of the game."""
        self.game_state = GameState.IN_PROGRESS
        self._generate_mines((x, y))
        self._reveal_safe_area(x, y)

    def _reveal_cell(self, x: int, y: int) -> None:
        """Reveal a single cell."""
        cell = self.grid[y][x]
        if cell.is_revealed or cell.is_flagged:
            return

        if cell.content == -1:
            self.game_state = GameState.LOST
            cell.is_revealed = True
            return

        self._flood_fill(x, y)
        self._check_win()

    def _chord_cell(self, x: int, y: int) -> None:
        """Perform a chord action on revealed numbered cells."""
        cell = self.grid[y][x]
        if not cell.is_revealed or cell.content == -1:
            return

        flagged = sum(
            1 for nx, ny in self._get_neighbors(x, y) if self.grid[ny][nx].is_flagged
        )
        if flagged == cell.content:
            for nx, ny in self._get_neighbors(x, y):
                self._reveal_cell(nx, ny)

    def _flag_cell(self, x: int, y: int) -> None:
        """Toggle flag on a cell."""
        cell = self.grid[y][x]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged
            return True


    def _check_win(self) -> None:
        """Check if the game has been won."""
        total_safe_cells = (self.level[0] * self.level[1]) - self.level[2]
        if self._revealed_count == total_safe_cells:
            self.game_state = GameState.WON

    def _reveal_safe_area(self, x: int, y: int, radius: int = 1) -> None:
        """Reveal an area around the given coordinate."""
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.level[0] and 0 <= ny < self.level[1]:
                    self._flood_fill(nx, ny)

    def make_move(self, coordinate: COORDINATE, move: Move) -> int:
        """Process a move and return number of newly revealed tiles."""
        revealed_before = self._revealed_count
        x, y = coordinate

        if self.moves == 0:
            self.moves += 1
            self._handle_first_move(x, y)
            return self._revealed_count - revealed_before

        match move:
            case Move.REVEAL:
                self._reveal_cell(x, y)
                cells_revealed = self._revealed_count - revealed_before
                if cells_revealed:
                    self.moves += 1
                return cells_revealed
            case Move.CHORD:
                self._chord_cell(x, y)
                cells_revealed = self._revealed_count - revealed_before
                if cells_revealed:
                    self.moves += 1
                return cells_revealed
            case Move.FLAG:
                return self._flag_cell(x, y)

    def reset(self, new_level: GameLevel = None) -> None:
        """Reset the game with optional new level."""
        self.moves = 0
        self.game_state = GameState.NOT_STARTED
        self._revealed_count = 0
        self._mine_locations = set()
        if new_level:
            self.level = new_level
            self.grid = [
                [Cell((x, y)) for x in range(self.level[0])]
                for y in range(self.level[1])
            ]
            
