from uiautomator import device as d
from AngelicaAI.textgen_messaging import TextgenMessaging
import sys
import os
from time import sleep
from random import randint

# Adjust the Python path to find the AngelicaAI module.


class InstagramChatbot:
    def __init__(self):
        # Initialize the TextgenMessaging instance.
        self.textgen_messaging = TextgenMessaging()

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
        """
        Open the messages page on Instagram.
        """
        d(resourceId="com.instagram.android:id/action_bar_inbox_button").click()
        self.wait()

    def get_last_message(self):
        """
        Get the last message in the chat.
        """
        # You can adjust this logic based on the UI hierarchy of the chat.
        # Here's a placeholder:
        message_elements = d(
            resourceId="com.instagram.android:id/message_content")
        return message_elements[-1].text if message_elements.exists else None

    def send_message(self, message):
        """
        Send a message in the chat.
        """
        # Placeholder logic based on common chat UI. Adjust as needed.
        text_field = d(resourceId="com.instagram.android:id/text_input")
        send_button = d(resourceId="com.instagram.android:id/send_button")

        if text_field.exists:
            text_field.set_text(message)
            if send_button.exists:
                send_button.click()
                self.wait()
