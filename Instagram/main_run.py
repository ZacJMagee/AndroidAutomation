import logging
import os
from dotenv import load_dotenv
from Instagram.instagram import InstagramChatbot, CommentInteractions, InstagramActions
from datetime import datetime
from .utils import random_sleep

load_dotenv()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("urllib3").setLevel(logging.WARNING)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")


def main():
    chatbot = InstagramChatbot(supabase_url, supabase_key)
    comment_interactions = CommentInteractions(chatbot)
    instagram_actions = InstagramActions()

    chatbot.open_instagram()
    random_sleep()

    if instagram_actions.check_for_new_messages():
        chatbot.open_messages()
        users_with_new_messages = chatbot.list_new_messages()
        for username in users_with_new_messages:
            chatbot.open_specific_chat(username)

            last_message = chatbot.get_last_message(username)
            if last_message:
                timestamp = datetime.now()
                conversation_id = username

                chatbot.store_message(
                    conversation_id, last_message, timestamp, "user")
                response = chatbot.respond_to_last_message([last_message])
                chatbot.wait(1, 2)

                if response:
                    chatbot.store_message(
                        conversation_id, response, timestamp, "bot")

            chatbot.close_chat()

        chatbot.close_messages()
        random_sleep()

    # Comment interactions
    total_comments = comment_interactions.get_total_comments()
    if total_comments == 0:
        logging.info("No comments found to interact with.")
        logging.info("Trying to scroll until comment section is visible...")
        comment_interactions.scroll_until_comment_section_visible()
        total_comments = comment_interactions.get_total_comments()
        if total_comments == 0:
            logging.info("Still no comments found after scrolling.")
            return

    comments_to_like = comment_interactions.calculate_likes(total_comments)
    comment_interactions.open_comment_section()  # Open the comment section

    random_sleep()

    comments_with_keywords = comment_interactions.get_comments_with_keywords(
        ["😊", "👍", "❤️", "🥰", "😘", "😍", "😎"])
    liked_count = comment_interactions.like_comments_based_on_criteria(
        comments_with_keywords, 0, comments_to_like)
    logging.info(f"Liked {liked_count} comments based on criteria.")

    # Do not close Instagram, continue with other actions if needed
    # chatbot.close_instagram()


if __name__ == "__main__":
    main()
