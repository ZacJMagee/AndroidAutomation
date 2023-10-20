from uiautomator import device as d
# Assuming you renamed the file after translating to UIautomator
from Instagram.instagram import InstagramActions, CommentInteractions
from utils import random_wait
import random


try:
    instagram_actions = InstagramActions()

    instagram_actions.open_instagram()
    random_wait(3)

    comment_interactions = CommentInteractions()

    for _ in range(3):  # This loop ensures the comment section is found and comments are liked three times
        # Reset processed comments at the start of each iteration
        comment_interactions.processed_comments.clear()

        # Scroll until the comment section is visible
        comment_interactions.scroll_until_comment_section_visible()
        random_wait(1)

        total_comments = comment_interactions.get_total_comments()
        print(f"Total Number of comments: {total_comments}")

        comments_to_like = min(50, random.randint(int(0.5 * total_comments)))
        print(f"Number of comments to like: {comments_to_like}")

        comment_interactions.open_comment_section()
        random_wait(2)

        liked_so_far = 0
        consecutive_empty_batches = 0
        max_consecutive_empty = 2

        # Capture and like comments in small batches multiple times
        for _ in range(5):  # Adjust the range as needed
            comment_data = comment_interactions.capture_comments(
                batches=4, liked_count=liked_so_far, max_likes=comments_to_like)
            print("Captured comments:", [comment[0]
                  for comment in comment_data])

            if not comment_data:
                consecutive_empty_batches += 1
                if consecutive_empty_batches >= max_consecutive_empty:
                    print("Detected hidden or inaccessible comments. Moving on...")
                    break
            else:
                consecutive_empty_batches = 0  # Reset if there are comments in the batch

            liked_so_far += len([comment for comment in comment_data if comment[0]
                                in comment_interactions.processed_comments])
            random_wait(2)

            if liked_so_far >= comments_to_like:
                break

        comment_interactions.close_comment_section()
        print(f"Comment Section Closed!")
        random_wait(3)

    instagram_actions.navigate_to_home_feed()
    print(f"Navigated Home!")
    random_wait(2)

except Exception as e:
    print('Error:', e)
