from typing import Literal,Tuple
from enum import IntEnum,Enum
from dataclasses import dataclass
from string import Template
from typing import Optional,Dict




TILE_STATE = Literal['hidden','revealed','highlight','victory','loss']
GAME_TITLE_TEMPLATE = 'MINESWEEPER {}X{}'
DIGIT_COLOR = {
    0: "transparent",
    1: "blue",
    2: "green",
    3: "red",
    4: "magenta",
    5: "firebrick",
    6: "cyan",
    7: "black",
    8: "grey"
}

COORDINATE = Tuple[int, int]

WIDTH, HEIGHT, MINES = int,int,int
LEVEL = Tuple[WIDTH, HEIGHT, MINES]


stat_view_template = {
    "win_streak": "{} WS",
    "win_rate": "{}% WR",
    "best_time": "{} BT",
    "games_played": "{} T",
    "games_lost": "{} L",
    "games_won": "{} W",
}


DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Chording(IntEnum):
    DISABLED: int = 0
    LEFT_CLICK: int = 1
    MIDDLE_CLICK: int = 2
    RIGHT_CLICK: int = 3


class GameState(IntEnum):
    NOT_STARTED = 0
    IN_PROGRESS = 2
    WON  = 1
    LOST = -1


class Move(IntEnum):
    REVEAL:int = 0
    FLAG:int = -1
    CHORD:int = 1



class GameLevel(Enum):

    CLASSIC:LEVEL = (8,8,9)
    EASY:LEVEL    = (9,9,10)
    MEDIUM:LEVEL  = (16,16,40)
    EXPERT:LEVEL  = (30,16,99)

    @classmethod
    def get_level_name(self,level):
        if level in [self.CLASSIC.value,self.EASY.value,self.MEDIUM.value,self.EXPERT.value]:
            return GameLevel(level).name
      
    
    @classmethod
    def values(cls):
        return [cls.CLASSIC.value,cls.EASY.value,cls.MEDIUM.value,cls.EXPERT.value]



@dataclass
class GameStat:
    """Statistics for a single game level."""

    win_streak: int = 0
    longest_win_streak: int = 0
    win_rate: float = 0.0
    best_time: Optional[int] = None
    previous_time: Optional[int] = None
    games_played: int = 0
    games_won: int = 0
    games_lost: int = 0


Statistics = Dict[Tuple[int, int, int], GameStat]


@dataclass
class ThemeEmote:
    idle  :str
    click :str
    lost  :str
    win   :str
    flag  :str
    mine  :str
    misflag :str

@dataclass
class GameTheme:
    '''base class for all themes'''
    name:str
    primary_tile:str
    secondary_tile:str
    victory_flag_tile:str
    primary_bomb_tile:str
    emote:ThemeEmote

