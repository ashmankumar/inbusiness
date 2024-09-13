import os
import signal

from src.ScreenRecorderModel import ScreenRecorderModel

if __name__ == '__main__':
    os.chdir('..')

    model = ScreenRecorderModel()

    model.set_up_recorder()
    model.start_listeners()

    # Set up signal handlers
    signal.signal(signal.SIGINT, model.stop_recording)
    signal.signal(signal.SIGTERM, model.stop_recording)
