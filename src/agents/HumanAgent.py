from src.agents.BaseAgent import BaseAgent
import pygame
import msvcrt
import sys

if sys.platform == 'win32':
    import msvcrt
    getch = msvcrt.getch
    getche = msvcrt.getche
else:
    import sys
    import termios
    def __gen_ch_getter(echo):
        def __fun():
            fd = sys.stdin.fileno()
            oldattr = termios.tcgetattr(fd)
            newattr = oldattr[:]
            try:
                if echo:
                    # disable ctrl character printing, otherwise, backspace will be printed as "^?"
                    lflag = ~(termios.ICANON | termios.ECHOCTL)
                else:
                    lflag = ~(termios.ICANON | termios.ECHO)
                newattr[3] &= lflag
                termios.tcsetattr(fd, termios.TCSADRAIN, newattr)
                ch = sys.stdin.read(1)
                if echo and ord(ch) == 127: # backspace
                    # emulate backspace erasing
                    # https://stackoverflow.com/a/47962872/404271
                    sys.stdout.write('\b \b')
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, oldattr)
            return ch
        return __fun
    getch = __gen_ch_getter(False)
    getche = __gen_ch_getter(True)


class HumanAgents(BaseAgent):
    def __init__(self):
        super().__init__()
        self.name = "human"
        self.x = None
        self.y = None

    def select_action(self):
        key = getche().decode()
        print(type(key))
        print(self.x, self.y)
        return int(key)