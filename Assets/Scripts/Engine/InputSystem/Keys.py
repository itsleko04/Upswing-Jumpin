from enum import Enum


class MouseButton(Enum):
    LEFT = 1
    RIGHT = 2
    MIDDLE = 3


class KeyPressStatus(Enum):
    PRESSED = 0
    RELEASED = 1
    HOLDING = 2


class Key:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.status: KeyPressStatus = KeyPressStatus.RELEASED

    def __repr__(self):
        return f"Key({self.name}, status={self.status.name})"


# МЫШЬ
MOUSE_LEFT = Key("MOUSE_LEFT", MouseButton.LEFT)
MOUSE_RIGHT = Key("MOUSE_RIGHT", MouseButton.RIGHT)
MOUSE_MIDDLE = Key("MOUSE_MIDDLE", MouseButton.MIDDLE)

# СИСТЕМНЫЕ
ESCAPE = Key("ESCAPE", 65307)
SPACE = Key("SPACE", 32)
ENTER = Key("ENTER", 65293)
TAB = Key("TAB", 65289)
BACKSPACE = Key("BACKSPACE", 65288)
LCTRL = Key("LCTRL", 65507)
LSHIFT = Key("LSHIFT", 65505)
LALT = Key("LALT", 65513)

# СТРЕЛКИ
UP_ARROW = Key("UP_ARROW", 65362)
DOWN_ARROW = Key("DOWN_ARROW", 65364)
LEFT_ARROW = Key("LEFT_ARROW", 65361)
RIGHT_ARROW = Key("RIGHT_ARROW", 65363)

# БУКВЫ
A = Key("A", 97)
B = Key("B", 98)
C = Key("C", 99)
D = Key("D", 100)
E = Key("E", 101)
F = Key("F", 102)
G = Key("G", 103)
H = Key("H", 104)
I = Key("I", 105)
J = Key("J", 106)
K = Key("K", 107)
L = Key("L", 108)
M = Key("M", 109)
N = Key("N", 110)
O = Key("O", 111)
P = Key("P", 112)
Q = Key("Q", 113)
R = Key("R", 114)
S = Key("S", 115)
T = Key("T", 116)
U = Key("U", 117)
V = Key("V", 118)
W = Key("W", 119)
X = Key("X", 120)
Y = Key("Y", 121)
Z = Key("Z", 122)

# ЦИФРЫ (ВЕРХНИЙ РЯД)
KEY_0 = Key("KEY_0", 48)
KEY_1 = Key("KEY_1", 49)
KEY_2 = Key("KEY_2", 50)
KEY_3 = Key("KEY_3", 51)
KEY_4 = Key("KEY_4", 52)
KEY_5 = Key("KEY_5", 53)
KEY_6 = Key("KEY_6", 54)
KEY_7 = Key("KEY_7", 55)
KEY_8 = Key("KEY_8", 56)
KEY_9 = Key("KEY_9", 57)

# ФУНКЦИОНАЛЬНЫЕ
F1 = Key("F1", 65470)
F2 = Key("F2", 65471)
F3 = Key("F3", 65472)
F4 = Key("F4", 65473)
F5 = Key("F5", 65474)
F6 = Key("F6", 65475)
F7 = Key("F7", 65476)
F8 = Key("F8", 65477)
F9 = Key("F9", 65478)
F10 = Key("F10", 65479)
F11 = Key("F11", 65480)
F12 = Key("F12", 65481)

# СПИСКИ
ALL_MOUSE_BUTTONS = [MOUSE_LEFT, MOUSE_RIGHT, MOUSE_MIDDLE]

ALL_KEYBOARD_KEYS = [
    ESCAPE, SPACE, ENTER, TAB, BACKSPACE, LCTRL, LSHIFT, LALT,
    UP_ARROW, DOWN_ARROW, LEFT_ARROW, RIGHT_ARROW,
    A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z,
    KEY_0, KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8, KEY_9,
    F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12
]

ALL_INPUT = ALL_MOUSE_BUTTONS + ALL_KEYBOARD_KEYS