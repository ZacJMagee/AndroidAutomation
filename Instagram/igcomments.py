from uiautomator import device as d
import random
import re
import logging
from .utils import random_sleep
from .services import InstagramActions

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')



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

