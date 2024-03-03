from rest_framework.decorators import api_view
from rest_framework.response import Response
from uiautomator import device as d
import re 
import logging 
from Instagram.utils import random_sleep 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')

@api_view(['GET'])
def open_instagram_view(request):
    try:
        d.press.home()
        random_sleep(4)
        d(text="Instagram").click()
        random_sleep()
        logging.info("Instagram Opened")
        return Response({'status': 'success', 'message': 'Instagram Opened'})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

@api_view(['GET'])
def close_instagram_view(request):
    try:
        d.press.home()
        logging.info("Instagram Closed")
        return Response({'status': 'success', 'message': 'Instagram Closed'})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

@api_view(['GET'])
def check_new_messages_view(request):
    try:
        inbox_button = d(resourceId="com.instagram.android:id/action_bar_inbox_button")
        if inbox_button.wait.exists(timeout=10000):
            content_desc = inbox_button.info.get('contentDescription', '')
            match = re.search(r'(\d+) unread message', content_desc)
            if match:
                num_unread_messages = int(match.group(1))
                logging.info(f"You have {num_unread_messages} unread message(s).")
                return Response({'new_messages': num_unread_messages})
            else:
                logging.info("No New Messages.")
                return Response({'new_messages': 0})
        else:
            logging.error("Inbox Button Not Found")
            return Response({'status': 'error', 'message': 'Inbox Button Not Found'}, status=404)
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

@api_view(['GET'])
def navigate_to_home_feed_view(request):
    try:
        d(resourceId='com.instagram.android:id/feed_tab').click()
        logging.info("Navigated to home feed")
        return Response({'status': 'success', 'message': 'Navigated to home feed'})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for checking if a post is sponsored
@api_view(['GET'])
def is_post_sponsored_view(request):
    try:
        sponsored_label = d(textContains="Sponsored")
        is_sponsored = sponsored_label.exists
        return Response({'is_sponsored': is_sponsored})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for finding the next like button
@api_view(['GET'])
def find_next_like_button_view(request):
    try:
        like_button = d(descriptionContains="Like")
        like_button_exists = like_button.exists
        return Response({'like_button_exists': like_button_exists})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for liking a post
@api_view(['GET'])
def like_post_view(request):
    try:
        like_button = d(descriptionContains="Like")
        if like_button.exists:
            like_button.click()
            logging.info("Post liked")
            return Response({'status': 'success', 'message': 'Post liked'})
        else:
            logging.warning("Like button not found")
            return Response({'status': 'warning', 'message': 'Like button not found'}, status=404)
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)
