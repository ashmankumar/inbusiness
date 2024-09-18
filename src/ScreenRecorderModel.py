import logging
import os
import shutil
import sys
from datetime import datetime
from multiprocessing import Event
from time import sleep

import pyautogui
from PIL import ImageDraw
from pynput import mouse, keyboard

from src.Utils import load_key_from_config

APP_TMP_DIR = 'tmp'

# Determine the base directory where the application is running
if getattr(sys, 'frozen', False):  # Check if the script is bundled by PyInstaller
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Constants
square_size = 150


class ScreenRecorderModel:
    def __init__(self):
        self.screenshot_count = 0
        self.stop_event = Event()
        self.app_tmp_dir = APP_TMP_DIR

    @staticmethod
    def take_full_screenshot(self):
        # Generate a filename with a timestamp
        return pyautogui.screenshot()

    def take_screenshot_localised(self, click_x, click_y):

        screenshot_region_px_size = float(load_key_from_config("screenshot_region_px_size"))

        if screenshot_region_px_size == 0:
            screenshot = self.take_full_screenshot()
            filename = self.save_screenshot(screenshot)
            print(f"Screenshot saved as {filename} for full resolution")

        region_x = max(click_x - screenshot_region_px_size // 2, 0)
        region_y = max(click_y - screenshot_region_px_size // 2, 0)
        screen_width, screen_height = pyautogui.size()
        region_width = min(screenshot_region_px_size, screen_width - region_x)
        region_height = min(screenshot_region_px_size, screen_height - region_y)
        screenshot = pyautogui.screenshot(region=(int(region_x), int(region_y), int(region_width), int(region_height)))
        draw = ImageDraw.Draw(screenshot)
        square_x = click_x - region_x - square_size // 2
        square_y = click_y - region_y - square_size // 2
        draw.rectangle([square_x, square_y, square_x + square_size, square_y + square_size], outline="red", width=2)
        filename = self.save_screenshot(screenshot)
        print(f"Screenshot saved as {filename} in the region around ({click_x}, {click_y})")

    def save_screenshot(self, screenshot):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        full_path = os.path.join(APP_TMP_DIR, filename)
        screenshot.save(full_path)
        return filename

    def on_click(self, x, y, button, pressed):
        if pressed:
            logging.info(f"Mouse clicked at ({x}, {y})")
            self.take_screenshot_localised(x, y)

    def on_press(self, key):
        try:
            if key == keyboard.Key.enter:
                self.take_full_screenshot()
            if key == keyboard.Key.esc:
                self.stop_event.set()
        except AttributeError:
            pass

    def start_listeners(self):
        mouse.Listener(on_click=self.on_click).start()
        logging.info("Recording started")

        # Keep the application running until the stop event is set
        while not self.stop_event.is_set():
            # Sleep to reduce CPU usage
            sleep(1)

    # Model: Handles the logic and data
    def stop_listeners(self):
        logging.info("Listeners stopped")
        mouse.Listener.stop()

    def set_up_recorder(self):
        self.clear_tmp_dir()
        print(f"Temporary directory {self.app_tmp_dir} cleared and recorder set up.")

    def clear_tmp_dir(self):
        print(f"Current working directory: {os.getcwd()}")
        try:
            if not os.path.exists(self.app_tmp_dir):
                os.makedirs(self.app_tmp_dir)
                print(f"Temporary directory created: {self.app_tmp_dir}")
            else:
                print(f"Temporary directory already exists: {self.app_tmp_dir}")

            for file_name in os.listdir(self.app_tmp_dir):
                file_path = os.path.join(self.app_tmp_dir, file_name)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        except Exception as e:
            print(f'Failed to create directory {self.app_tmp_dir}. Reason: {e}')

    def stop_recording(self, signum, frame):
        print(f"Signal {signum} received. Stopping recording...")
        self.stop_event.set()
