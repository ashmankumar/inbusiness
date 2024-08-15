from abc import ABC, abstractmethod
from typing import List


class LLMInterface(ABC):
    @abstractmethod
    def check_frames(self, prompt: str, resolution: str, tokens: int, images_base64: List[str], json_response_model) -> str:
        """
        Method to check frames using an LLM.

        Args:
            prompt (str): The prompt to send to the LLM.
            resolution (str): The desired resolution for the image processing.
            tokens (int): The maximum number of tokens for the response.
            images_base64 (List[str]): List of images in base64 format.

        Returns:
            str: The response from the LLM.
            :param images_base64: 
            :param json_response_model: 
        """
        pass
