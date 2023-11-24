import httpx
import uuid
from dotenv import load_dotenv
from supabase import create_client, Client
import os
import hashlib
import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "apikey": SUPABASE_KEY,
}


class SupabaseHandler:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def get_or_create_conversation(self, username):
        # Check if a conversation with this username already exists
        existing_conversation = self.supabase.table("conversations").select(
            "conversation_id").eq("username", username).execute()

        if existing_conversation.data:
            # Conversation exists, return the existing ID
            return existing_conversation.data[0]['conversation_id']
        else:
            # Conversation does not exist, create a new one
            new_conversation_data = {
                "username": username,
                "conversation_id": str(uuid.uuid4())
            }
            new_conversation = self.supabase.table("conversations").insert(
                new_conversation_data).execute()
            return new_conversation.data[0]['conversation_id']

    def store_message(self, username: str, message_text: str, timestamp: datetime.datetime, sender: str):
        try:
            # Ensure timestamp is in the correct format
            timestamp_str = timestamp.strftime(
                '%Y-%m-%d %H:%M:%S') if isinstance(timestamp, datetime.datetime) else str(timestamp)

            # Generate a hash of the message text and timestamp
            message_hash = hashlib.sha256(
                f"{message_text}{timestamp_str}".encode()).hexdigest()

            # Get or create the conversation and retrieve the UUID
            conversation_id = self.get_or_create_conversation(username)

            # Check if the message already exists
            existing_message = self.supabase.table("messages").select(
                "*").eq("hash", message_hash).execute()
            if existing_message.data:
                print("Message already exists.")
                return

            # The message is new, store it
            message_data = {
                "conversation_id": conversation_id,
                "message_text": message_text,
                "timestamp": timestamp_str,
                "sender": sender,
                "hash": message_hash
            }
            self.supabase.table("messages").insert(message_data).execute()

            # Update the last message timestamp in the Conversations table
            self.supabase.table("conversations").update({"last_message_timestamp": timestamp_str}).eq(
                "conversation_id", conversation_id).execute()

            print("Message stored successfully.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Failed to store message or retrieve conversation ID.")

    def get_recent_messages(self, conversation_id: str, limit: int = 10):
        messages = self.supabase.table("messages").select(
            "*").eq("conversation_id", conversation_id).limit(limit).execute()
        return messages.data
