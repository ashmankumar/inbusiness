import os

from src.ScreenRecorderModel import ScreenRecorderModel

if __name__ == '__main__':
    os.chdir('..')

    model = ScreenRecorderModel()

    model.set_up_recorder()
    model.start_listeners()
