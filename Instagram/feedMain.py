from uiautomator import device as d
from Instagram.instagram import InstagramActions
from utils import random_wait


def main():
    instagram_actions = InstagramActions()

    instagram_actions.open_instagram()
    random_wait(4, 6)

    posts_liked = 0
    posts_to_like = 5

    while posts_liked < posts_to_like:
        # Check if the post is sponsored
        if instagram_actions.is_post_sponsored():
            # Find the next like button
            like_button = instagram_actions.find_next_like_button()
            if like_button.exists:
                # Get the bounds of the like button
                bounds = like_button.info["bounds"]
                # Scroll the like button out of view
                d.swipe(520, bounds["bottom"] + 10, 520, 300, steps=30)
            else:
                # If the like button isn't found, perform a usual scroll
                d.swipe(520, 1100, 520, 400, steps=30)

            random_wait(2, 4)
        else:
            # If the post isn't sponsored, try to like it
            if instagram_actions.like_post():
                posts_liked += 1
                print(f"Liked {posts_liked} posts so far.")

            # Scroll to the next post
            d.swipe(520, 1100, 520, 400, steps=30)
            random_wait(2, 4)

    instagram_actions.close_instagram()


if __name__ == "__main__":
    main()
