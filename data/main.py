

from .control import Control

def main(fullscreen, size):
    app = Control(fullscreen, size)
    app.run()
