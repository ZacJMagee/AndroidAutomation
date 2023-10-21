import logging
from uiautomator import device as d
from AngelicaAI.textgen_messaging import TextgenMessaging
from AngelicaAI.supabase_handler import SupabaseHandler
from time import sleep
from random import randint


class InstagramChatbot:
    def __init__(self):
        self.d = d
        self.logger = logging.getLogger(__name__)
        try:
            self.textgen_messaging = TextgenMessaging()
            logging.info("TextgenMessaging initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing TextgenMessaging: {e}")
        self.supabase_handler = SupabaseHandler()
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

    def list_usernames(self):
        usernames = d(resourceId="com.instagram.android:id/row_inbox_username")
        user_list = [user.text for user in usernames]
        logging.info(
            f"Detected {len(user_list)} usernames: {', '.join(user_list)}")
        return user_list

    def open_specific_chat(self, username):
        self.logger.info(f"Attempting to open chat with {username}...")
        chat_element = self.d(descriptionContains=username,
                              resourceId="com.instagram.android:id/row_inbox_container")
        if chat_element.exists:
            chat_element.click()
            self.logger.info(f"Chat with {username} opened successfully.")
        else:
            self.logger.warning(f"Chat element for {username} not found.")

    def get_username(self):
        return d(resourceId="com.instagram.android:id/row_thread_title_textview").text

    def get_last_message(self, selected_username):
        messages = d(
            resourceId="com.instagram.android:id/row_thread_message_textview")
        return messages[-1].text if messages else None

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
        response = self.textgen_messaging.send_message_and_get_response(
            messages[-1], messages)
        self.send_message(response)

    def fetch_latest_chat_history(self, username):
        return self.supabase_handler.get_chat_history(username)

    def store_messages(self, messages):
        username = self.get_username()
        self.supabase_handler.save_chat_history(
            username, {"history": messages})


if __name__ == "__main__":
    bot = InstagramChatbot()
    # Sample usage or testing can be added here
