"""Constants for the pygame GUI: colours, sizes, fonts."""

WINDOW_W = 1180
WINDOW_H = 720
FPS = 60

# Board geometry
CELL = 84
BOARD_ORIGIN = (40, 130)
DISC_PADDING = 6
GRAVITY = 1.6  # px per frame^2 in the drop animation

# Tree panel
TREE_RECT = (680, 20, 480, 680)
TREE_LINE_HEIGHT = 22
TREE_HEADER_HEIGHT = 34

# Colours
BG = (24, 26, 32)
PANEL = (34, 37, 46)
BOARD_BLUE = (30, 70, 160)
HOLE = (24, 26, 32)
HUMAN_COLOUR = (230, 70, 70)
AI_COLOUR = (240, 200, 50)
TEXT = (235, 235, 240)
TEXT_DIM = (140, 145, 160)
MAX_COLOUR = (240, 200, 50)
MIN_COLOUR = (240, 120, 120)
PRUNED_COLOUR = (100, 105, 120)
BUTTON = (55, 60, 75)
BUTTON_HOVER = (75, 82, 102)
BUTTON_SELECTED = (60, 120, 220)

# Fonts (None = pygame default)
FONT_NAME = None
FONT_SMALL = 18
FONT_MEDIUM = 24
FONT_LARGE = 44
TREE_FONT_NAMES = "menlo,consolas,dejavusansmono,couriernew"
TREE_FONT_SIZE = 14
