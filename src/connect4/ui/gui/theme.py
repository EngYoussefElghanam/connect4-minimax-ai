"""Constants for the pygame GUI: colours, sizes, fonts."""

WINDOW_W = 1180
WINDOW_H = 720
FPS = 60

# Board geometry
DISC_PADDING = 6
GRAVITY = 1.6  # px per frame^2 in the drop animation

# Colours
MAX_COLOUR = (240, 200, 50)
MIN_COLOUR = (240, 120, 120)
PRUNED_COLOUR = (100, 105, 120)

# Fonts (None = pygame default)
FONT_NAME = None
FONT_SMALL = 18
FONT_MEDIUM = 24
FONT_LARGE = 44
TREE_FONT_NAMES = "menlo,consolas,dejavusansmono,couriernew"
TREE_FONT_SIZE = 14

# Tabletop palette
BG = (248, 244, 231)
PANEL = (255, 253, 245)
TEXT = (31, 44, 59)
TEXT_DIM = (79, 92, 102)
BOARD_BLUE = (44, 90, 158)
HOLE = (25, 51, 91)
HUMAN_COLOUR = (235, 94, 74)
AI_COLOUR = (249, 193, 59)
BUTTON = (245, 243, 231)
BUTTON_HOVER = (225, 231, 225)
BUTTON_SELECTED = (39, 76, 98)
EDGE = (200, 203, 190)
CAP_BLUE = BOARD_BLUE
BOW_PINK = HUMAN_COLOUR
BOARD_ORIGIN = (44, 166)
CELL = 76
TREE_RECT = (630, 108, 516, 574)
TREE_HEADER_HEIGHT = 75
TREE_LINE_HEIGHT = 56
