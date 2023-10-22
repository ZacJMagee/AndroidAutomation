import logging
from Instagram.instaChatbot import InstagramChatbot
from time import sleep

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


logging.getLogger("urllib3").setLevel(logging.WARNING)


def main():

    # Initialize the chatbot
    chatbot = InstagramChatbot()

    chatbot.open_specific_chat("Zac Magee")

    sleep(3)

    # Attempt to retrieve the last message
    last_message = chatbot.get_last_message("Zac Magee")
    if last_message:
        print(f"Last message from Zac: {last_message}")

        # Generate a response using TextgenMessaging
        response = chatbot.textgen_messaging.send_message(
            last_message, [last_message])

        print(f"Generated response: {response}")

        # Send the generated response
        chatbot.send_message(response)
        print("Response sent!")
    else:
        print("No messages found in the chat")


if __name__ == "__main__":
    main()
