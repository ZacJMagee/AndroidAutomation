import logging
import os
from dotenv import load_dotenv
from Instagram.instagram import InstagramChatbot
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("urllib3").setLevel(logging.WARNING)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")


def main():
    chatbot = InstagramChatbot(supabase_url, supabase_key)

    users_with_new_messages = chatbot.list_new_messages()

    for username in users_with_new_messages:
        chatbot.open_specific_chat(username)
        last_message = chatbot.get_last_message(username)
        if last_message:
            timestamp = datetime.now()
            conversation_id = username

            chatbot.store_message(
                conversation_id, last_message, timestamp, "user")
            response = chatbot.respond_to_last_message([last_message])
            chatbot.wait(1, 2)
            # Ensure the response is stored
            if response:
                chatbot.store_message(
                    conversation_id, response, timestamp, "bot")

        chatbot.close_chat()


if __name__ == "__main__":
    main()
