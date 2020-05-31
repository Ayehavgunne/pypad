NONE = 0x00  # No key pressed

LCTRL = 0x01
CTRL = LCTRL
LSHIFT = 0x02
SHIFT = LSHIFT
LALT = 0x04
ALT = LALT
LMETA = 0x08
META = LMETA
RCTRL = 0x10
RSHIFT = 0x20
RALT = 0x40
RMETA = 0x80

MOD_CODES = [LCTRL, LSHIFT, LALT, LMETA, RCTRL, RSHIFT, RALT, RMETA]
MOD_NAMES = [
    "SHIFT",
    "LSHIFT",
    "RSHIFT",
    "CTRL",
    "LCTRL",
    "RCTRL",
    "ALT",
    "LALT",
    "RALT",
    "META",
    "LMETA",
    "RMETA",
]

ERR_OVF = 0x01  # Keyboard Error Roll Over - used for all slots if too many keys are pressed ("Phantom key")

A = 0x04  # Keyboard a and A
B = 0x05  # Keyboard b and B
C = 0x06  # Keyboard c and C
D = 0x07  # Keyboard d and D
E = 0x08  # Keyboard e and E
F = 0x09  # Keyboard f and F
G = 0x0A  # Keyboard g and G
H = 0x0B  # Keyboard h and H
I = 0x0C  # Keyboard i and I
J = 0x0D  # Keyboard j and J
K = 0x0E  # Keyboard k and K
L = 0x0F  # Keyboard l and L
M = 0x10  # Keyboard m and M
N = 0x11  # Keyboard n and N
O = 0x12  # Keyboard o and O
P = 0x13  # Keyboard p and P
Q = 0x14  # Keyboard q and Q
R = 0x15  # Keyboard r and R
S = 0x16  # Keyboard s and S
T = 0x17  # Keyboard t and T
U = 0x18  # Keyboard u and U
V = 0x19  # Keyboard v and V
W = 0x1A  # Keyboard w and W
X = 0x1B  # Keyboard x and X
Y = 0x1C  # Keyboard y and Y
Z = 0x1D  # Keyboard z and Z

NUM1 = 0x1E  # Keyboard 1 and !
NUM2 = 0x1F  # Keyboard 2 and @
NUM3 = 0x20  # Keyboard 3 and #
NUM4 = 0x21  # Keyboard 4 and $
NUM5 = 0x22  # Keyboard 5 and %
NUM6 = 0x23  # Keyboard 6 and ^
NUM7 = 0x24  # Keyboard 7 and &
NUM8 = 0x25  # Keyboard 8 and *
NUM9 = 0x26  # Keyboard 9 and (
NUM0 = 0x27  # Keyboard 0 and )

ENTER = 0x28  # Keyboard Return (ENTER)
ESC = 0x29  # Keyboard ESCAPE
BACKSPACE = 0x2A  # Keyboard Backspace
TAB = 0x2B  # Keyboard Tab
SPACE = 0x2C  # Keyboard Spacebar
MINUS = 0x2D  # Keyboard - and _
EQUAL = 0x2E  # Keyboard = and +
LEFT_BRACE = 0x2F  # Keyboard [ and {
RIGHT_BRACE = 0x30  # Keyboard ] and }
BACKSLASH = 0x31  # Keyboard \ and |
SEMICOLON = 0x33  # Keyboard ; and :
APOSTROPHE = 0x34  # Keyboard ' and "
GRAVE = 0x35  # Keyboard ` and ~
COMMA = 0x36  # Keyboard , and <
DOT = 0x37  # Keyboard . and >
SLASH = 0x38  # Keyboard / and ?
CAPS_LOCK = 0x39  # Keyboard Caps Lock

F1 = 0x3A  # Keyboard F1
F2 = 0x3B  # Keyboard F2
F3 = 0x3C  # Keyboard F3
F4 = 0x3D  # Keyboard F4
F5 = 0x3E  # Keyboard F5
F6 = 0x3F  # Keyboard F6
F7 = 0x40  # Keyboard F7
F8 = 0x41  # Keyboard F8
F9 = 0x42  # Keyboard F9
F10 = 0x43  # Keyboard F10
F11 = 0x44  # Keyboard F11
F12 = 0x45  # Keyboard F12

PRINT_SCREEN = 0x46  # Keyboard Print Screen
SCROLL_LOCK = 0x47  # Keyboard Scroll Lock
PAUSE = 0x48  # Keyboard Pause
# INSERT = 0x49  # Keyboard Insert, I hate INSERT. I will not allow it!
HOME = 0x4A  # Keyboard Home
PAGE_UP = 0x4B  # Keyboard Page Up
DELETE = 0x4C  # Keyboard Delete
END = 0x4D  # Keyboard End
PAGE_DOWN = 0x4E  # Keyboard Page Down
RIGHT = 0x4F  # Keyboard Right Arrow
LEFT = 0x50  # Keyboard Left Arrow
DOWN = 0x51  # Keyboard Down Arrow
UP = 0x52  # Keyboard Up Arrow

NUMLOCK = 0x53  # Keyboard Num Lock and Clear
KEYPAD_SLASH = 0x54  # Keypad /
KEYPAD_ASTERISK = 0x55  # Keypad *
KEYPAD_MINUS = 0x56  # Keypad -
KEYPAD_PLUS = 0x57  # Keypad +
KEYPAD_ENTER = 0x58  # Keypad ENTER
KEYPAD_1 = 0x59  # Keypad 1 and End
KEYPAD_2 = 0x5A  # Keypad 2 and Down Arrow
KEYPAD_3 = 0x5B  # Keypad 3 and PageDn
KEYPAD_4 = 0x5C  # Keypad 4 and Left Arrow
KEYPAD_5 = 0x5D  # Keypad 5
KEYPAD_6 = 0x5E  # Keypad 6 and Right Arrow
KEYPAD_7 = 0x5F  # Keypad 7 and Home
KEYPAD_8 = 0x60  # Keypad 8 and Up Arrow
KEYPAD_9 = 0x61  # Keypad 9 and Page Up
KEYPAD_0 = 0x62  # Keypad 0 and Insert
KEYPAD_DOT = 0x63  # Keypad . and Delete

COMPOSE = 0x65  # Keyboard Application
POWER = 0x66  # Keyboard Power

F13 = 0x68  # Keyboard F13
F14 = 0x69  # Keyboard F14
F15 = 0x6A  # Keyboard F15
F16 = 0x6B  # Keyboard F16
F17 = 0x6C  # Keyboard F17
F18 = 0x6D  # Keyboard F18
F19 = 0x6E  # Keyboard F19
F20 = 0x6F  # Keyboard F20
F21 = 0x70  # Keyboard F21
F22 = 0x71  # Keyboard F22
F23 = 0x72  # Keyboard F23
F24 = 0x73  # Keyboard F24

OPEN = 0x74  # Keyboard Execute
HELP = 0x75  # Keyboard Help
PROPS = 0x76  # Keyboard Menu
FRONT = 0x77  # Keyboard Select
STOP = 0x78  # Keyboard Stop
AGAIN = 0x79  # Keyboard Again
UNDO = 0x7A  # Keyboard Undo
CUT = 0x7B  # Keyboard Cut
COPY = 0x7C  # Keyboard Copy
PASTE = 0x7D  # Keyboard Paste
FIND = 0x7E  # Keyboard Find
MUTE = 0x7F  # Keyboard Mute
VOLUME_UP = 0x80  # Keyboard Volume Up
VOLUME_DOWN = 0x81  # Keyboard Volume Down

KEYPAD_LEFT_PAREN = 0xB6  # Keypad (
KEYPAD_RIGHT_PAREN = 0xB7  # Keypad )

LEFT_CTRL = 0xE0  # Keyboard Left Control
LEFT_SHIFT = 0xE1  # Keyboard Left Shift
LEFT_ALT = 0xE2  # Keyboard Left Alt
LEFT_META = 0xE3  # Keyboard Left GUI
RIGHT_CTRL = 0xE4  # Keyboard Right Control
RIGHT_SHIFT = 0xE5  # Keyboard Right Shift
RIGHT_ALT = 0xE6  # Keyboard Right Alt
RIGHT_META = 0xE7  # Keyboard Right GUI

MEDIA_PLAY_PAUSE = 0xE8
MEDIA_STOP_CD = 0xE9
MEDIA_PREVIOUS_SONG = 0xEA
MEDIA_NEXT_SONG = 0xEB
MEDIA_EJECT_CD = 0xEC
MEDIA_VOLUME_UP = 0xED
MEDIA_VOLUME_DOWN = 0xEE
MEDIA_MUTE = 0xEF
MEDIA_WWW = 0xF0
MEDIA_BACK = 0xF1
MEDIA_FORWARD = 0xF2
MEDIA_STOP = 0xF3
MEDIA_FIND = 0xF4
MEDIA_SCROLL_UP = 0xF5
MEDIA_SCROLL_DOWN = 0xF6
MEDIA_EDIT = 0xF7
MEDIA_SLEEP = 0xF8
MEDIA_COFFEE = 0xF9
MEDIA_REFRESH = 0xFA
MEDIA_CALC = 0xFB
