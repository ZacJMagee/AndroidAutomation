import os
import requests
import json
import html
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TextgenMessaging:
    def __init__(self):
        self.TEXTGEN_API_URL = "http://127.0.0.1:5000/v1/chat/completions"
        self.HEADERS = {
            "Content-Type": "application/json"
        }

    def send_message(self, user_input, history):
        data = {
            "mode": "chat",
            "character": "Angelica",
            "messages": [{"role": "user", "content": user_input}] + history
        }
        response = requests.post(
            self.TEXTGEN_API_URL,
            headers=self.HEADERS,
            json=data
        )
        return self._handle_response(response)

    def _handle_response(self, response):
        try:
            data = response.json()
            assistant_message = data['choices'][0]['message']['content']
            return html.unescape(assistant_message)  # Unescape here
        except (json.JSONDecodeError, IndexError, KeyError):
            raise Exception(
                "Error decoding JSON or extracting the generated message.")
