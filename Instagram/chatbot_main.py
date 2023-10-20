from instagram_chatbot import InstagramChatbot
from utils import random_sleep


def main():
    # Create an instance of InstagramChatbot
    chatbot = InstagramChatbot()

    # Open Instagram
    chatbot.open_instagram()

    # Wait for a random time to allow Instagram to load properly
    random_sleep(3, 10)

    # Check for new messages
    if chatbot.has_new_messages():
        # If new messages exist, click to open messages
        chatbot.open_messages()

    print("Script stopped.")


if __name__ == "__main__":
    main()
