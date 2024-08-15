import base64
import os
from io import BytesIO
from typing import List

import cv2
import numpy as np
from PIL import Image
import logging

from .AI.LLMInterface import LLMInterface
from .AI.OpenAIClient import OpenAIClient
from .model.PydanticModels import Process

from .Constants import APP_TMP_DIR


# Logic class for handling screen processing and AI interaction
class ScreenRecordAnalyser:
    def __init__(self):
        # Initialize any required parameters
        pass

    def load_images_from_folder(self, folder_path: str) -> List[np.ndarray]:
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                img_path = os.path.join(folder_path, filename)
                image = Image.open(img_path)
                frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                frames.append(frame)
        return frames

    def down_size_images(self, frames: List[np.ndarray], width: int, height: int) -> List[np.ndarray]:
        resized_frames = []
        for frame in frames:
            resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            resized_frames.append(resized_frame)
        return resized_frames

    def encode_frames_to_base64(self, frames: List[np.ndarray]) -> List[str]:
        encoded_frames = []
        for frame in frames:
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            encoded_frame = base64.b64encode(buffered.getvalue()).decode('utf-8')
            encoded_frames.append(encoded_frame)
        return encoded_frames

    def get_analysis_of_images(self, folder_path: str, client: LLMInterface, task_description: str):
        frames = self.load_images_from_folder(folder_path)
        resized_images = self.down_size_images(frames, 512, 512)
        encoded_frames = self.encode_frames_to_base64(resized_images)

        logging.info('Encoded frames: %d', len(encoded_frames))
        logging.info('Initializing OpenAI client...')

        logging.info('Checking frames with LLM ...')
        response = client.check_frames(
            prompt=self.get_prompt(task_description),
            resolution="low",
            tokens=10000,
            images_base64=encoded_frames,
            json_response_model=Process
        )
        return response

    @staticmethod
    def get_prompt(task_description: str) -> str:
        return (
            "You are an AI that meticulously records user a business process flow by looking at screenshots of actions. "
            "These are frames from a screen recording showing a user conducting work for the task with description: {}. "
            "A red circle indicates the user has clicked. Provide a description of the overall task or tasks, and the low level actions the user undertakes as part of them. Write sentences as instructions. "
            "Only return actions or tasks where you have very high confidence, don't ever guess and purely narrate "
            "what the user does, think critically. If you see a red circle without a button it means the users has probably incorrectly clicked. Ignore these."
        ).format(task_description)


# Example usage of the ScreenProcessingLogic class
if __name__ == "__main__":
    logic = ScreenRecordAnalyser()
    client = OpenAIClient()

    response = logic.get_analysis_of_images(APP_TMP_DIR, client)
    print(response)
