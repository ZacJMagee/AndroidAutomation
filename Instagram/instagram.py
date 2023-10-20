from uiautomator import device as d
import re
from utils import random_wait


class InstagramActions:
    def __init__(self):
        pass

    def open_instagram(self):
        d.press.home()
        d(text="Instagram").click()

    def close_instagram(self):
        d.press.home()

    def navigate_to_home_feed(self):
        d(resourceId='com.instagram.android:id/feed_tab').click()


class CommentInteractions:
    def __init__(self):
        super().__init__()
        self.processed_comments = set()

    def scroll_until_comment_section_visible(self, max_tries=10):
        tries = 0
        while not self.find_comment_section() and tries < max_tries:
            d.swipe(525, 1105, 565, 625, steps=30)
            random_wait(1, 2)
            tries += 1

    def get_total_comments(self):
        comment_section = self.find_comment_section()
        if comment_section:
            text = comment_section.text
            match = re.search(r'(\d+)', text)
            if match:
                return int(match.group(1))
        return 0

    def open_comment_section(self):
        comment_section = self.find_comment_section()
        if comment_section:
            comment_section.click()
            random_wait(3, 4)

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

                    liked_count = self.like_comments_based_on_criteria(
                        comments, liked_count, max_likes)

                    current_comments = set([comment[0]
                                           for comment in comments])
                    if current_comments == previous_comments:
                        repetitive_count += 1
                        if repetitive_count >= 2:
                            return all_comments
                    else:
                        repetitive_count = 0

                    previous_comments = current_comments
                    break

                except Exception:  # UIautomator doesn't have StaleElementReferenceException, so a general exception is used
                    print("Encountered an error. Re-finding elements...")
                    comment_elements = d(
                        resourceId='com.instagram.android:id/row_comment_textview_comment')

            d.swipe(500, 1165, 515, 680, steps=30)

        return all_comments

    def get_comments_with_keywords(self, keywords):
        """Extract comments containing specific keywords from the current post."""
        comments = []

        # Assuming the comment element has a resource id of 'commentId' (this needs to be adjusted)
        comment_elements = d(resourceId='commentId')

        for comment_element in comment_elements:
            comment_text = comment_element.text
            if any(keyword in comment_text for keyword in keywords):
                comments.append(comment_text)

        return comments

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
            print(f"Successfully liked the comment: '{comment_element.text}'.")

        except ValueError:
            print(
                f"Error: The comment '{comment_element.text}' is not in the current view")

        except Exception:  # Catching general exceptions in case the like button isn't found or any other issues arise
            print(
                f"Error: Like button not found for the comment: '{comment_element.text}'.")

    def close_comment_section(self):
        d.press.back()

    def is_in_comment_section(self):
        return d.exists(resourceId='com.instagram.android:id/layout_comment_thread_edittext')

    def recover_from_disruption(self):
        d.press.back()
        random_wait(1, 2)
        if not self.is_in_comment_section():
            print("Recovery Failed. Restarting sequence for this post.")
            self.close_comment_section()
            self.scroll_until_comment_section_visible()
            self.open_comment_section()
