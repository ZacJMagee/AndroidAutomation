import logging
import random
from Instagram.instaChatbot import InstagramChatbot
from time import sleep


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.getLogger("urllib3").setLevel(logging.WARNING)


def main():
    # Initialize the chatbot
    chatbot = InstagramChatbot()

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

            # Generate a response using TextgenMessaging
            response = chatbot.textgen_messaging.send_message(
                last_message, [last_message])

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
