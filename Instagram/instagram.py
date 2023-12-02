from uiautomator import device as d
import random
import re
import logging
from .utils import random_sleep
from time import time
from AngelicaAI.textgen_messaging import TextgenMessaging
from AngelicaAI.supabase_handler import SupabaseHandler

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


class CommentInteractions(InstagramActions):
    def __init__(self, chatbot):
        self.chatbot = chatbot
        super().__init__()
        self.processed_comments = set()

    def find_comment_section(self):
        comment_section = d(
            resourceId='com.instagram.android:id/row_feed_view_all_comments_text')
        if comment_section.exists:
            return comment_section
        return None

    def scroll_until_comment_section_visible(self, max_tries=10):
        tries = 0
        while tries < max_tries:
            comment_section = self.find_comment_section()
            if comment_section:
                logging.info("Comment section found!")
                return
            else:
                logging.info("Comment section not found. Swiping...")
                d.swipe(525, 1105, 565, 625, steps=30)
                random_sleep(1, 2)
                tries += 1
        logging.warning("Reached maximum tries. Comment section not found.")

    def get_total_comments(self):
        comment_section = self.find_comment_section()
        if comment_section:
            text = comment_section.text
            match = re.search(r'(\d+)', text)
            if match:
                return int(match.group(1))
        return 0

    def calculate_likes(self, total_comments):
        total_comments = self.get_total_comments()
        if total_comments == 0:
            logging.info("No comments found on the post.")
            return

        # Calculate the number of comments to like
        # At least 1 like or 20% of total comments
        min_likes = max(int(total_comments * 0.20), 1)
        # At most 80% of total comments or 50 likes
        max_likes = min(int(total_comments * 0.80), 50)
        comments_to_like = random.randint(min_likes, max_likes)

        logging.info(f"Total comments: {total_comments}")
        logging.info(f"Planning to like {comments_to_like} comments.")

        return comments_to_like

    def open_comment_section(self):
        comment_section = self.find_comment_section()
        if comment_section:
            comment_section.click()
            random_sleep(3, 4)
            logging.info("Opened comment section")

    def capture_comments(self, batches=1, liked_count=0, max_likes=None):
        all_comments = []
        previous_comments = set()
        repetitive_count = 0

        for _ in range(batches):
            comments = []

            if not self.is_in_comment_section():
                self.recover_from_disruption()

            for attempt in range(3):
                try:
                    comment_elements = d(
                        resourceId='com.instagram.android:id/row_comment_textview_comment')
                    for element in comment_elements:
                        if element.text not in self.processed_comments:
                            comments.append((element.text, element))
                            self.processed_comments.add(element.text)

                    # Like comments based on criteria
                    liked_count = self.like_comments_based_on_criteria(
                        comments, liked_count, max_likes)
                    if max_likes is not None and liked_count >= max_likes:
                        return all_comments, liked_count

                    current_comments = set([comment[0]
                                           for comment in comments])
                    if current_comments == previous_comments:
                        repetitive_count += 1
                        if repetitive_count >= 2:
                            return all_comments, liked_count
                    else:
                        repetitive_count = 0

                    previous_comments = current_comments
                    break

                except Exception:
                    logging.error(
                        "Encountered an error. Re-finding elements...")
                    comment_elements = d(
                        resourceId='com.instagram.android:id/row_comment_textview_comment')

            d.swipe(500, 1165, 515, 680, steps=30)

        return all_comments, liked_count

    def get_comments_with_keywords(self, keywords, batches=2):
        all_comments = set()
        extracted_comments = []

        for _ in range(batches):
            comment_elements = d(
                resourceId='com.instagram.android:id/row_comment_textview_comment')
            for comment_element in comment_elements:
                comment_text = comment_element.text
                if comment_text not in all_comments:
                    all_comments.add(comment_text)
                    if any(keyword in comment_text for keyword in keywords):
                        extracted_comments.append(comment_text)
                        logging.info(
                            f"Extracted comment with keywords: {comment_text}")

            # Scroll to load more comments
            d.swipe(500, 1000, 500, 500, steps=10)
            random_sleep  # Wait for comments to load

        logging.info(
            f"Extracted {len(extracted_comments)} comments with specified keywords.")
        return extracted_comments

    def like_comments_based_on_criteria(self, comments, liked_count, max_likes):
        keywords = ["😊", "👍", "❤️", "🥰", "😘", "😍", "🤤"]
        for comment_text, comment_element in comments:
            if liked_count >= max_likes:
                return liked_count
            for keyword in keywords:
                if keyword in comment_text:
                    self.like_comment(comment_element)
                    liked_count += 1
                    break
        logging.info(f"Liked {liked_count} comments based on criteria.")
        return liked_count

    def like_comment(self, comment_element):
        try:
            all_comment_elements = d(
                resourceId='com.instagram.android:id/row_comment_textview_comment')
            all_like_buttons = d(
                resourceId='com.instagram.android:id/row_comment_like_button_click_area')
            comment_index = all_comment_elements.index(comment_element)
            like_button = all_like_buttons[comment_index]
            like_button.click()
            logging.info(
                f"Successfully liked the comment: '{comment_element.text}'.")
        except ValueError:
            logging.error(
                f"Error: The comment '{comment_element.text}' is not in the current view.")
        except Exception:
            logging.error(
                f"Error: Like button not found for the comment: '{comment_element.text}'.")

    def close_comment_section(self):
        d.press.back()
        logging.info("Closed comment section.")

    def is_in_comment_section(self):
        in_section = d.exists(
            resourceId='com.instagram.android:id/layout_comment_thread_edittext')
        return in_section

    def recover_from_disruption(self):
        d.press.back()
        random_sleep(1, 2)
        if not self.is_in_comment_section():
            logging.warning(
                "Recovery Failed. Restarting sequence for this post.")
            self.close_comment_section()
            self.scroll_until_comment_section_visible()
            self.open_comment_section()


class InstagramChatbot:
    def __init__(self, supabase_url, supabase_key):
        self.instagram_actions = InstagramActions()
        self.d = d
        self.logger = logging.getLogger(__name__)
        try:
            self.supabase_handler = SupabaseHandler(supabase_url, supabase_key)
            self.textgen_messaging = TextgenMessaging()  # No parameters required here
            logging.info("TextgenMessaging initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing TextgenMessaging: {e}")
        logging.info("Supabase initialized")

    def open_instagram(self):
        return self.instagram_actions.open_instagram()

    def wait(self, min_seconds=5, max_seconds=10):
        random_sleep(min_seconds, max_seconds)

    def open_messages(self):
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
            else:
                logging.info("No new messages.")

            # Click the inbox button to open messages
            inbox_button.click()
            logging.info("Messages opened")
        else:
            logging.error("Inbox button not found")

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

    # Sample usage or testing can be added here
