import httpx
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "apikey": SUPABASE_API_KEY,
}


class SupabaseHandler:

    @staticmethod
    async def get_chat_history(user_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/chat_histories?username=eq.{user_id}",
                headers=HEADERS
            )
            if response.status_code == 200 and response.json():
                return response.json()[0].get("history", {})
            else:
                print(
                    f"Error retrieving chat history from Supabase: {response.status_code}")
                return {}

    @staticmethod
    async def save_chat_history(user_id: str, chat_data: dict):
        async with httpx.AsyncClient() as client:
            # Prepare the data to insert or update
            data = {
                "username": user_id,
                "history": chat_data
            }

            # Try to insert new data
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/chat_histories",
                json=data,
                headers=HEADERS
            )

            if response.status_code != 201:
                print(
                    f"Error saving chat history to Supabase: {response.status_code}")
                print(f"Supabase response when saving: {response.json()}")
