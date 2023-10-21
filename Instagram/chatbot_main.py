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
    print("Available usernames to interact with:")
    usernames = chatbot.list_usernames()
    for idx, username in enumerate(usernames, start=1):
        print(f"{idx}. {username}")

    choice = int(input("Enter the number corresponding to the username: "))
    if 1 <= choice <= len(usernames):
        selected_username = usernames[choice-1]

        # Open the selected chat
        chatbot.open_specific_chat(selected_username)

        # Fetch the last message and generate a response
        logging.info(
            f"Fetching the last message from chat with {selected_username}...")
        last_message = chatbot.get_last_message()
        if last_message:
            logging.info(
                f"Last message from {selected_username}: {last_message}")
            response = chatbot.textgen_messaging.send_message_and_get_response(
                last_message)
            chatbot.send_message(response)
            logging.info(f"Sent response to {selected_username}: {response}")
        else:
            logging.warning(
                f"No messages found in the chat with {selected_username}.")
    else:
        logging.error("Invalid choice. Exiting.")


def main():
    chatbot = initialize_chatbot()
    print("Available usernames to interact with:")
    usernames = chatbot.list_usernames()
    for idx, username in enumerate(usernames, 1):
        print(f"{idx}. {username}")

    choice = int(input("Enter the number corresponding to the username: "))
    if 1 <= choice <= len(usernames):
        selected_username = usernames[choice - 1]
        interact_with_user(chatbot, selected_username)
    else:
        print("Invalid choice. Exiting.")
    logging.info("Script stopped.")


if __name__ == "__main__":
    main()
