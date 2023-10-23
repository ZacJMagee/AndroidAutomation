import logging
from uiautomator import device as d
from AngelicaAI.textgen_messaging import TextgenMessaging
from AngelicaAI.supabase_handler import SupabaseHandler
from time import sleep
from random import randint


class InstagramChatbot:
    def __init__(self, supabase_url, supabase_key):
        self.d = d
        self.logger = logging.getLogger(__name__)
        try:
            self.supabase_handler = SupabaseHandler(supabase_url, supabase_key)
            self.textgen_messaging = TextgenMessaging()  # No parameters required here
            logging.info("TextgenMessaging initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing TextgenMessaging: {e}")
        logging.info("Supabase initialized")

    def wait(self, min_seconds=5, max_seconds=10):
        sleep(randint(min_seconds, max_seconds))

    def open_instagram(self):
        d.press.home()
        self.wait(2, 4)
        d(text="Instagram").click()
        self.wait()

    def open_messages(self):
        d(description="Direct").click()
        self.wait()

    def list_new_messages(self):
        usernames_with_new_messages = []
        try:
            chat_containers = d(
                resourceId="com.instagram.android:id/row_inbox_container")
            if not chat_containers.wait.exists(timeout=10000):
                self.logger.error("Chat containers not found.")
                return usernames_with_new_messages

            for chat_container in chat_containers:
                username_element = chat_container.child(
                    resourceId="com.instagram.android:id/row_inbox_username")
                if not username_element.wait.exists(timeout=10000):
                    self.logger.error("Username element not found.")
                    continue

                content_desc = chat_container.info.get(
                    'contentDescription', '')
                if 'unread' in content_desc and username_element.exists:
                    usernames_with_new_messages.append(username_element.text)
                    self.logger.debug(
                        f"New message indicator found for user: {username_element.text}")
                else:
                    self.logger.debug(
                        f"No new message indicator found for user: {username_element.text}")

            self.logger.info(
                f"Detected new messages from: {', '.join(usernames_with_new_messages)}")
        except Exception as e:
            self.logger.error(f"Error in list_new_messages: {e}")

        return usernames_with_new_messages

    def open_specific_chat(self, username):
        logging.debug("Entered open_specific_chat function...")
        print("Entered open_specific_chat function...")  # Direct print
        try:
            logging.debug(f"Attempting to open chat with {username}...")
            # Direct print
            print(f"Attempting to open chat with {username}...")

            # Find the chat element based on resource-id and content-desc containing the username
            chat_element = self.d(resourceId="com.instagram.android:id/row_inbox_container",
                                  descriptionMatches=f"^{username},.*")

            # Check if the chat element exists and click it
            if chat_element.exists:
                logging.debug("Chat element exists. Trying to click...")
                print("Chat element exists. Trying to click...")  # Direct print
                chat_element.click()
                logging.debug(f"Opened chat with {username}...")
                print(f"Opened chat with {username}...")  # Direct print
            else:
                logging.warning(f"Chat element for {username} not found!")
                # Direct print
                print(f"Chat element for {username} not found!")

        except Exception as e:
            logging.error(
                f"Error while trying to open chat with {username}: {e}")
            # Direct print
            print(f"Error while trying to open chat with {username}: {e}")

    def get_username(self):
        return d(resourceId="com.instagram.android:id/row_thread_title_textview").text

    def get_last_message(self, username):
        try:
            # Find the message elements based on the provided resource-id
            message_elements = self.d(
                resourceId="com.instagram.android:id/direct_text_message_text_view")

            # Log the number of message elements found
            logging.debug(f"Found {len(message_elements)} message elements.")

            # If message elements are found, iterate in reverse to find the last valid message
            if message_elements.exists:
                for i in range(len(message_elements) - 1, -1, -1):
                    message = message_elements[i].text
                    if message:
                        return message
                logging.warning(
                    f"No valid messages found in the chat with {username}.")
                return None
            else:
                logging.warning(
                    f"No messages found in the chat with {username}.")
                return None
        except Exception as e:
            logging.error(f"Error fetching last message from {username}: {e}")
            return None

    def send_message(self, message):
        try:
            text_field = d(
                resourceId="com.instagram.android:id/row_thread_composer_edittext")
            if text_field.exists:
                text_field.set_text(message)
                send_button = d(
                    resourceId="com.instagram.android:id/row_thread_composer_button_send")
                if send_button.exists:
                    send_button.click()
                    self.wait(1, 2)
                else:
                    logging.warning("Send button not found.")
            else:
                logging.warning("Text input field not found.")
        except Exception as e:
            logging.error(f"Error while trying to send message: {e}")

    def respond_to_last_message(self, messages):
        response = self.textgen_messaging.send_message(messages[-1], messages)
        self.send_message(response)
        return response

    def fetch_latest_chat_history(self, username):
        return self.supabase_handler.get_chat_history(username)

    def store_message(self, conversation_id, message_text, timestamp, sender):
        self.supabase_handler.store_message(
            conversation_id, message_text, timestamp, sender)

    def get_recent_messages(self, conversation_id, limit=10):
        return self.supabase_handler.get_recent_messages(conversation_id, limit)

    def close_chat(self):
        try:
            back_button = self.d(
                resourceId="com.instagram.android:id/action_bar_button_back")
            if back_button.exists:
                back_button.click()
                self.wait(1, 2)
            else:
                self.logger.warning(
                    "Back button not found. Could not close the chat.")
        except Exception as e:
            self.logger.error(f"Error while trying to close the chat: {e}")


if __name__ == "__main__":
    bot = InstagramChatbot()
    # Sample usage or testing can be added here
