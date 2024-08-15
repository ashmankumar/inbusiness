from openai import OpenAI
from typing import List

from .LLMInterface import LLMInterface
import os
import yaml


class OpenAIClient(LLMInterface):
    def __init__(self):
        self.client = OpenAI(api_key=self.load_key_from_config())

    """
    Grab the open_api_key from the config file.
    Check environment variables if the key is not found in the config file.
    Throw an error if the key is not found in the config file or environment variables.
    """
    @staticmethod
    def load_key_from_config() -> str:

        # Load the OpenAI API key from the config.yaml file
        try:
            with open('config.yml', 'r') as file:
                config = yaml.safe_load(file)
                api_key = config.get('open_api_key')
        except FileNotFoundError:
            api_key = None

        # Check environment variables if the key is not found in the config file
        if not api_key:
            api_key = os.getenv('OPEN_API_KEY')

        # Throw an error if the key is not found in the config file or environment variables
        if not api_key:
            raise ValueError("OpenAI API key not found in config file or environment variables")

        return api_key

    def check_frames(self, prompt: str, resolution: str, tokens: int, images_base64: List[str], json_response_model) -> str:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ]
            }
        ]

        # Adding images to the messages
        for img_base64 in images_base64:
            messages[0]["content"].append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{img_base64}",
                        "detail": resolution
                    }
                }
            )

        if json_response_model is not None:

            # Sending the request to OpenAI API
            response = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=tokens,
                response_format=json_response_model
            )

        else:
            # Sending the request to OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=tokens,
            )

        # Returning the LLM response
        return response.choices[0].message.content