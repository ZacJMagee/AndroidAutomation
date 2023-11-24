from AngelicaAI.textgen_messaging import TextgenMessaging
from AngelicaAI.supabase_handler import SupabaseHandler
import datetime
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

def main():
    textgen = TextgenMessaging()
    supabase_handler = SupabaseHandler(SUPABASE_URL, SUPABASE_KEY)
    username = "test_user"
    user_input = "Hello, how are you?"
    history = []
    response = textgen.send_message(user_input, history)
    print(response)
    timestamp = datetime.datetime.now()
    supabase_handler.store_message(username, user_input, timestamp, "user")
    supabase_handler.store_message(username, response, timestamp, "assistant")

if __name__ == "__main__":
    main()
