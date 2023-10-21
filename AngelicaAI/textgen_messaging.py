import os
import requests
import json
import html
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TextgenMessaging:
    def __init__(self):
        self.TEXTGEN_API_URL = os.getenv(
            'TEXTGEN_API_URL')
        self.HEADERS = {
            "Content-Type": "application/json"
        }

    def send_message(self, user_input, history):
        data = {
            "user_input": user_input,
            "mode": "chat",
            "character": "Angelica1",
            "state": {
                "history": history
            }
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
            visible_history = data.get('results', [{}])[0].get(
                'history', {}).get('visible', [])
            generated_text = visible_history[-1][1] if visible_history else 'No response from TextgenAI'
            return html.unescape(generated_text)  # Unescape here
        except (json.JSONDecodeError, IndexError, KeyError):
            raise Exception(
                "Error decoding JSON or extracting the generated message.")
