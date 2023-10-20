import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TextgenMessaging:
    TEXTGEN_API_URL = os.getenv(
        'TEXTGEN_API_URL')
    HEADERS = {
        "Content-Type": "application/json"
    }

    def send_message_and_get_response(self, user_input, history):
        """Send a message to TextgenAI and get a response."""

        # Prepare the request data
        data = {
            "user_input": user_input,
            "state": {
                "history": history
            }
        }

        # Make the POST request to TextgenAI API
        response = requests.post(
            self.TEXTGEN_API_URL,
            headers={
                'Content-Type': 'application/json',
            },
            json=data
        )

        return self._handle_response(response)

    def _handle_response(self, response):
        """Handle the response from TextgenAI API."""

        try:
            data = response.json()

            # Extract the generated message using the revised structure
            visible_history = data.get('results', [{}])[0].get(
                'history', {}).get('visible', [])
            generated_text = visible_history[-1][1] if visible_history else 'No response from TextgenAI'

            return generated_text

        except (json.JSONDecodeError, IndexError, KeyError):
            print(
                "Error decoding JSON or extracting the generated message: " + response.text)
            return "Error decoding response."
