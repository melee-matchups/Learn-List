import os


def init():
    if os.name == 'nt':  # Only if we are running on Windows
        from ctypes import windll
        k = windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11), 7)


class Style:
    UNDERLINE = "\033[4m"
    UNDERLINE_OFF = "\033[24m"

    BOLD = "\033[1m"


class Fg:
    BLUE = "\033[34m"
    WHITE = "\033[37m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_WHITE = "\033[97m"


RESET = "\033[0m"
