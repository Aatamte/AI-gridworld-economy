import os
from subprocess import Popen, PIPE, DEVNULL
from src.utils import get_render_path
import time
import signal
import contextlib


class ReactServer:
    def __init__(self):
        pass

    def start(self):
        cwd = os.getcwd()
        os.chdir(get_render_path())
        build = False
        if build:
            self.proc = Popen("serve -l 3000 -s build", shell=True)
        else:
            self.proc = Popen("npm run start", shell=True, stdin=PIPE, stdout=DEVNULL)
        os.chdir(cwd)
        time.sleep(2)

    def stop(self):
        # simulate pressing control c, Y to prompt to shutdown react server
        self.proc.send_signal(signal.CTRL_C_EVENT)
        self.proc.stdin.write(b"Y\n")
        self.proc.stdin.close()
        time.sleep(1)

        print("done")