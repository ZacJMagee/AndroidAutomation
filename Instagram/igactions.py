from uiautomator import device as d
import random
import re
import logging
from .utils import random_sleep

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class InstagramActions:
    # ... all methods of InstagramActions ...
from uiautomator import device as d
import random
import re
import logging
from .utils import random_sleep

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class InstagramActions:
    def __init__(self):
        pass

    def open_instagram(self):
        d.press.home()
        random_sleep(2, 4)  # Replacing the self.wait method
        d(text="Instagram").click()
        random_sleep()  # Default wait time between 5 to 15 seconds
        logging.info("Instagram opened")

    def close_instagram(self):
        d.press.home()
        logging.info("Instagram closed")

    def check_for_new_messages(self):
        # Wait for the inbox button to be visible
        inbox_button = d(
            resourceId="com.instagram.android:id/action_bar_inbox_button")
        if inbox_button.wait.exists(timeout=10000):  # wait for 10 seconds
            # Retrieve the content description
            content_desc = inbox_button.info.get('contentDescription', '')

            # Check for new messages
            match = re.search(r'(\d+) unread message', content_desc)
            if match:
                num_unread_messages = int(match.group(1))
                logging.info(
                    f"You have {num_unread_messages} unread message(s).")
                return True
            else:
                logging.info("No new messages.")
                return False
        else:
            logging.error("Inbox button not found")
            return False

    def navigate_to_home_feed(self):
        d(resourceId='com.instagram.android:id/feed_tab').click()
        logging.info("Navigated to home feed")

    def is_post_sponsored(self):
        # Logic to determine if a post is sponsored
        sponsored_label = d(textContains="Sponsored")
        return sponsored_label.exists

    def find_next_like_button(self):
        # Logic to find the next like button
        like_button = d(descriptionContains="Like")
        return like_button.exists

    def like_post(self):
        # Logic to like a post
        like_button = d(descriptionContains="Like")
        if like_button.exists:
            like_button.click()
            logging.info("Post liked")
        else:
            logging.warning("Like button not found")
