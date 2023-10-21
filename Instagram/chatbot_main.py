import logging
from Instagram.instaChatbot import InstagramChatbot

# Set up logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_chatbot():
    chatbot = InstagramChatbot()
    logging.info("InstagramChatbot initialized")
    return chatbot


def interact_with_user(chatbot, username):
    chatbot.open_specific_chat(username)
    logging.info(f"Opened chat with {username}.")
    messages = chatbot.read_messages_last_two()
    logging.info(f"Retrieved last two messages: {messages}")
    latest_history = chatbot.fetch_latest_chat_history(username)
    logging.info(f"Retrieved latest history from Supabase: {latest_history}")
    response = chatbot.respond_to_last_message(messages)
    logging.info(f"Generated response: {response}")
    chatbot.send_message(response)
    logging.info(f"Response sent to {username}'s chat.")
    chatbot.store_messages(messages)
    logging.info(f"Stored {len(messages)} messages to Supabase.")


def main():
    chatbot = initialize_chatbot()
    username = input("Enter the username to interact with: ")
    interact_with_user(chatbot, username)
    logging.info("Script stopped.")


if __name__ == "__main__":
    main()
