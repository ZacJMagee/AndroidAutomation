import logging
import random
import os
from dotenv import load_dotenv
from Instagram.instaChatbot import InstagramChatbot
from time import sleep
from AngelicaAI.supabase_handler import SupabaseHandler  # Import SupabaseHandler

load_dotenv()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.getLogger("urllib3").setLevel(logging.WARNING)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")


def main():
    # Initialize the chatbot
    chatbot = InstagramChatbot(supabase_url, supabase_key)

    # Check for new messages
    new_messages = chatbot.list_new_messages()

    # If there are new messages, process them
    for username in new_messages:
        chatbot.open_specific_chat(username)
        sleep(3)

        # Retrieve the last message from the user with a new message
        last_message = chatbot.get_last_message(username)
        if last_message:
            print(f"Last message from {username}: {last_message}")

            # Store the last message in Supabase
            chatbot.store_message(
                'conversation_id', last_message, 'timestamp', 'user')

            # Retrieve recent messages for this conversation from Supabase
            recent_messages = chatbot.get_recent_messages('conversation_id')
            print("Recent messages from Supabase:", recent_messages)

            # Generate a response using TextgenMessaging
            response = chatbot.generate_response(last_message, recent_messages)

            print(f"Generated response: {response}")

            # Send the generated response
            chatbot.send_message(response)
            print(f"Response sent to {username}!")

            sleep_duration = random.uniform(2, 5)
            sleep(sleep_duration)

            # Navigate back to the main chat menu
            chatbot.d(
                resourceId="com.instagram.android:id/action_bar_button_back").click()
            sleep(2)
        else:
            print(f"No messages found in the chat with {username}")


if __name__ == "__main__":
    main()
