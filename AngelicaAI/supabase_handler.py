import httpx
from dotenv import load_dotenv
from supabase import create_client, Client
import os
import hashlib

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "apikey": SUPABASE_API_KEY,
}


class SupabaseHandler:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def store_message(self, conversation_id: str, message_text: str, timestamp: str, sender: str):
        # Generate a hash of the message text and timestamp
        message_hash = hashlib.sha256(
            f"{message_text}{timestamp}".encode()).hexdigest()

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
            "timestamp": timestamp,
            "sender": sender,
            "hash": message_hash
        }
        self.supabase.table("messages").insert(message_data).execute()

        # Update the last message timestamp in the Conversations table
        self.supabase.table("conversations").update(
            {"last_message_timestamp": timestamp}).eq("id", conversation_id).execute()

    def get_recent_messages(self, conversation_id: str, limit: int = 10):
        messages = self.supabase.table("messages").select(
            "*").eq("conversation_id", conversation_id).order("timestamp", ascending=False).limit(limit).execute()
        return messages.data
