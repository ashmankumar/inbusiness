from openai import OpenAI
from typing import List

from .LLMInterface import LLMInterface
import os
import yaml

from ..Utils import load_key_from_config


class OpenAIClient(LLMInterface):
    def __init__(self):
        self.client = OpenAI(api_key=load_key_from_config(key='open_api_key'))

    def check_frames(self, prompt: str, resolution: str, tokens: int, images_base64: List[str],
                     json_response_model) -> str:
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
                model=load_key_from_config(key='model_name'),
                messages=messages,
                max_tokens=tokens,
            )

        # Returning the LLM response
        return response.choices[0].message.content
