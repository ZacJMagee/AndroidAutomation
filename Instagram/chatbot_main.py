import logging
from Instagram.instaChatbot import InstagramChatbot

# Set up logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_chatbot():
    try:
        chatbot = InstagramChatbot()
        logging.info("InstagramChatbot initialized")
        return chatbot
    except Exception as e:
        logging.error(f"Error initializing InstagramChatbot: {e}")
        return None


def interact_with_user(chatbot):
    usernames = chatbot.list_usernames()
    if not usernames:
        logging.warning("No usernames detected.")
        return

    print("Available usernames to interact with:")
    for idx, username in enumerate(usernames, 1):
        print(f"{idx}. {username}")

    choice = -1
    while choice not in range(1, len(usernames) + 1):
        try:
            choice = int(
                input("Enter the number corresponding to the username: "))
        except ValueError:
            pass

    selected_username = usernames[choice - 1]
    chatbot.open_specific_chat(selected_username)
    chatbot.wait(5, 7)  # Wait for a few seconds after opening the chat
    last_message = chatbot.get_last_message(selected_username)
    if last_message:
        response = chatbot.generate_response(last_message)
        chatbot.send_message(response)
    else:
        logging.warning(
            f"No messages found in the chat with {selected_username}.")


def main():
    chatbot = initialize_chatbot()
    if chatbot:
        interact_with_user(chatbot)
        logging.info("Script stopped.")


if __name__ == "__main__":
    main()
