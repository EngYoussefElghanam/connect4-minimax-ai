"""Hand-built boards shared by the tests. Row strings are TOP -> BOTTOM; 'H' human, 'A' AI, '.' empty.
FULL_* boards were brute-force verified: (AI fours, human fours) are noted next to each."""

EMPTY = ["......."] * 6

# Full boards (42 discs) -------------------------------------------------------
FULL_DRAW = [            # AI 0 - human 0
    "HHAHAAH", "HAAHAHH", "AAHAAHH", "AHHAHAA", "AAHAHAH", "HHAHHAA",
]
FULL_AI_WINS = [         # AI 2 - human 1
    "HHAHHAH", "HAAAHHH", "HAHAAHH", "AHHAHAA", "AAAHHAH", "HAAHAAA",
]
FULL_HUMAN_WINS = [      # AI 1 - human 3
    "HAAAHAH", "HAAAAHH", "HHHHAHA", "AHAAHHA", "AHAHHAH", "HHAHAAA",
]

# Single-feature boards ------------------------------------------------------------
def _bottom(row: str) -> list[str]:
    return ["......."] * 5 + [row]

AI_THREE_OPEN = _bottom(".AAA...")      # both ends playable
HUMAN_THREE_OPEN = _bottom(".HHH...")
AI_THREE_BLOCKED = _bottom("HAAAH..")   # no completing cell for anyone
AI_TWO = _bottom(".AA....")
AI_TWO_BLOCKED = _bottom("HAA....")
AI_ONE = _bottom("..A....")
AI_FOUR = _bottom("AAAA...")            # one four
AI_FIVE = _bottom("AAAAA..")            # two overlapping fours
HUMAN_FOUR = _bottom("HHHH...")
BOTH_FOUR = ["......."] * 4 + ["HHHH...", "AAAA..."]   # one four each
A_CENTRE = _bottom("...A...")
A_EDGE = _bottom("A......")
H_CENTRE = _bottom("...H...")
H_EDGE = _bottom("H......")

# AI to move; human threatens a vertical four in column index 3 (4th column)
VERTICAL_THREAT = [
    ".......", ".......", ".......",
    "...H...",
    "A..H..A",
    "A..H..A",
]

MID_GAME = [
    ".......", ".......", ".......",
    "...A...",
    "..HAH..",
    ".AHHA..",
]
