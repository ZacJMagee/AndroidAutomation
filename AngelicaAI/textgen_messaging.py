from supabase_py import create_client, Client
from datetime import datetime
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()


class TextgenMessaging:

    # Configuration for TextgenAI
    HOST = 'localhost:5000'  # Placeholder, should be updated with the actual host
    URI_CHAT = f'http://{HOST}/api/v1/chat'
    HEADERS = {
        "Content-Type": "application/json"
    }

    # Configuration for Supabase
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    # Replace with your actual API key
    SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

    def __init__(self):
        pass

    def send_message_and_get_response(self, user_input, history=None):
        """Send user input to TextgenAI and get a response."""
        request_data = self._construct_request(user_input, history)
        response = requests.post(
            self.URI_CHAT, headers=self.HEADERS, json=request_data)
        return self._handle_response(response)

    def _construct_request(self, user_input, history):
        """Construct the API request for TextgenAI."""
        request_data = {
            "user_input": user_input,
            "history": history if history else [],
            # ... [Other parameters, like mode, temperature, etc.]
        }
        return request_data

    def _handle_response(self, response):
        """Handle the response from TextgenAI."""

        # Print out the response status and text for debugging
        print(f"Response Status: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            try:
                data = response.json()
                return data.get("message", "")
            except json.JSONDecodeError:
                print("Failed to decode JSON. Returning raw response text.")
                return response.text
        else:
            return f"Error occurred with status {response.status_code}: {response.text}"

    def save_chat_history(self, user_id, history):
        """Save the chat history to the Supabase database."""
        timestamp = datetime.utcnow().isoformat()
        table = "chat_histories"
        data = {
            "user_id": user_id,
            "history": history,
            "timestamp": timestamp
        }
        response = self.supabase.table(table).insert(data)
        return response

    def retrieve_chat_history(self, user_id):
        """Retrieve the chat history for a user from the Supabase database."""
        table = "chat_histories"
        response = self.supabase.table(table).select().filter(
            'user_id', 'eq', user_id).order_by('timestamp', ascending=False).limit(1).single()
        return response.get('data', {}).get('history', {})
