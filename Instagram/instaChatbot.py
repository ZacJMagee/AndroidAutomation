from uiautomator import device as d
from AngelicaAI.textgen_messaging import TextgenMessaging
from AngelicaAI.supabase_handler import SupabaseHandler
import sys
from time import sleep
from random import randint

# Adjust the Python path to find the AngelicaAI module.
sys.path.append('/home/mrmagee/Projects/OFAutomation')

print("We are starting!")


class InstagramChatbot:
    def __init__(self):
        try:
            # Initialize the TextgenMessaging instance.
            print("InstagramChatbot: Before")
            self.textgen_messaging = TextgenMessaging()
            print("TextgenMessaging initialized successfully")
        except Exception as e:
            print(f"Error initializing TextgenMessaging: {e}")
        self.supabase_handler = SupabaseHandler()
        print("Supabase started")

    def wait(self, min_seconds=5, max_seconds=10):
        """
        Wait for a random time between min_seconds and max_seconds.
        """
        sleep(randint(min_seconds, max_seconds))

    def open_instagram(self):
        """
        Open the Instagram app.
        """
        d.press.home()
        self.wait(2, 4)
        d(text="Instagram").click()
        self.wait()

    def check_new_messages(self):
        """
        Check if there are new messages in the Instagram inbox.
        """
        # Check for new messages based on content description.
        new_message_element = d(descriptionContains="Unread")
        return new_message_element.exists

    def open_messages(self):
        """Open the Instagram messages page."""
        try:
            # Locate the element that represents the messages button based on its resource ID or content description.
            # Replace "YOUR_RESOURCE_ID" with the actual resource ID for the messages button.
            messages_button = d(resourceId="com.instagram.android:id/action_bar_inbox_button",
                                descriptionContains="unread message")
            if messages_button.exists:
                messages_button.click()
                self.wait()
            else:
                print("Messages button not found.")
        except Exception as e:
            print(f"Error opening messages: {e}")

    def list_usernames(self):
        try:

            username_elements = d(
                resourceId="com.instagram.android:id/row_inbox_username")

            usernames = [element.text for element in username_elements]

            for username in usernames:
                print(f"Found Username: {username}")

            return usernames
        except Exception as e:
            print(f"Error listing username")
            return []

    def get_username(self):
        username_element = d(
            resourceId="com.instagram.android:id/row_inbox_username", text="molly magee ˙ᵕ˙")
        return username_element.text if username_element.exists else None

    def get_last_message(self):
        """
        Get the last message in the chat.
        """
        # You can adjust this logic based on the UI hierarchy of the chat.
        # Here's a placeholder:
        message_elements = d(
            resourceId="com.instagram.android:id/message_content")
        return message_elements[-1].text if message_elements.exists else None

    def get_visible_messages_in_chat(self):
        """Get the visible messages in the current chat."""
        message_elements = d(
            resourceId="com.instagram.android:id/direct_text_message_text_view")
        return [message.text for message in message_elements] if message_elements.exists else []

    def generate_response_based_on_history(self, history):
        return self.textgen_messaging.send_message_and_get_response("", history)

    def send_generated_response(self, user):
        chat_history = self.supabase_handler.get_chat_history(user)

        # Prepare the request data
        data = {
            "user_input": ' '.join(chat_history),
            "state": {
                "history": chat_history
            }
        }

        # Send the request to TextgenAI and retrieve the response
        response = self.textgen_messaging.send_message_and_get_response(data)

        # Send the generated response as a message in the chat
        self.send_message(response)

    def send_message(self, message):
        """
        Send a message in the chat.
        """
        try:
            # Locate the text input field
            text_field = d(
                resourceId="com.instagram.android:id/row_thread_composer_edittext")

            # Set the message text
            if text_field.exists:
                text_field.set_text(message)

                # The send button should become visible after entering text
                send_button = d(
                    resourceId="com.instagram.android:id/row_thread_composer_button_send")

                # Click the send button
                if send_button.exists:
                    send_button.click()
                    self.wait(1, 2)  # Giving a brief pause after sending
                else:
                    print("Send button not found.")
            else:
                print("Text input field not found.")
        except Exception as e:
            print(f"Error while trying to send message: {e}")

    def open_specific_chat(self, username):
        """Open the chat of a specific user."""
        try:
            chat_element = d(
                resourceId="com.instagram.android:id/row_inbox_username", text=username)
            if chat_element.exists:
                chat_element.click()
                self.wait()
            else:
                print(f"Chat for user {username} not found.")
        except Exception as e:
            print(f"Error opening chat for user {username}: {e}")

    def respond_to_last_message(self):
        """Respond to the last message in the chat."""
        try:
            # Retrieve last message
            last_message = self.get_last_message()

            # Fetch chat history from Supabase
            chat_history = self.supabase_handler.get_chat_history(
                self.get_username())

            # Get a response from TextgenMessaging
            response = self.textgen_messaging.send_message_and_get_response(
                last_message, chat_history)

            # Send the response
            self.send_message(response)

            # Save chat history
            chat_data = {"last_message": last_message, "response": response}
            self.supabase_handler.save_chat_history(
                self.get_username(), chat_data)
        except Exception as e:
            print(f"Error responding to last message: {e}")

    def count_new_messages(self):
        """Count the number of new messages."""
        new_message_elements = d(
            resourceId="com.instagram.android:id/action_bar_inbox_button", descriptionContains="unread message")
        return len(new_message_elements) if new_message_elements.exists else 0

    def read_messages(self):
        """Read the last two messages in the current chat."""
        try:
            message_elements = d(
                resourceId="com.instagram.android:id/direct_text_message_text_view")
            if message_elements.exists:
                # Assuming the message_elements are in the order they appear on the screen
                # We only want the last two messages
                return [message.text for message in message_elements][-2:]
            else:
                print("No messages found.")
                return []
        except Exception as e:
            print(f"Error reading messages: {e}")
            return []

    def read_messages_last_two(self):
        """Read the last two messages in the current chat."""
        message_elements = d(
            resourceId="com.instagram.android:id/direct_text_message_text_view")
        all_messages = [
            message.text for message in message_elements] if message_elements.exists else []

        # Return the last two messages
        return all_messages[-2:] if len(all_messages) >= 2 else all_messages

    def fetch_latest_chat_history(self, user_id):
        """Fetch the latest chat history for a user from Supabase."""
        chat_history = self.supabase_handler.get_chat_history(user_id)
        return chat_history.get("history", []) if chat_history else []

    def store_messages(self, messages):
        """Store the messages to Supabase."""
        chat_data = {"messages": messages}
        self.supabase_handler.save_chat_history(self.get_username(), chat_data)

    def generate_response(self, user_input, history=[]):
        """
        Generate a response using the TextgenMessaging instance.

        Parameters:
        - user_input: The latest message from the user.
        - history: The conversation history.

        Returns:
        - The generated response.
        """
        try:
            return self.textgen_messaging.send_message_and_get_response(user_input, history)
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Error generating response."
