from rest_framework.decorators import api_view
from rest_framework.response import Response
from uiautomator import device as d
import re
import logging
from Instagram.utils import random_sleep
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# DRF view for finding the comment section
@api_view(['GET'])
def find_comment_section_view(request):
    try:
        comment_section = d(resourceId='com.instagram.android:id/row_feed_view_all_comments_text')
        if comment_section.exists:
            logging.info("Comment section found")
            return Response({'status': 'success', 'message': 'Comment section found'})
        logging.info("Comment section not found")
        return Response({'status': 'warning', 'message': 'Comment section not found'}, status=404)
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for scrolling until the comment section is visible
@api_view(['GET'])
def scroll_until_comment_section_visible_view(request):
    try:
        max_tries = request.GET.get('max_tries', 10)
        tries = 0
        while tries < int(max_tries):
            comment_section = d(resourceId='com.instagram.android:id/row_feed_view_all_comments_text')
            if comment_section.exists:
                logging.info("Comment section found!")
                return Response({'status': 'success', 'message': 'Comment section found'})
            else:
                logging.info("Comment section not found. Swiping...")
                d.swipe(525, 1105, 565, 625, steps=30)
                random_sleep(1, 2)
                tries += 1
        logging.warning("Reached maximum tries. Comment section not found.")
        return Response({'status': 'warning', 'message': 'Comment section not found after maximum tries'}, status=404)
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for getting the total number of comments
@api_view(['GET'])
def get_total_comments_view(request):
    try:
        comment_section = d(resourceId='com.instagram.android:id/row_feed_view_all_comments_text')
        if comment_section.exists:
            text = comment_section.text
            match = re.search(r'(\d+)', text)
            if match:
                total_comments = int(match.group(1))
                return Response({'total_comments': total_comments})
        return Response({'total_comments': 0})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for opening the comment section
@api_view(['GET'])
def open_comment_section_view(request):
    try:
        comment_section = d(resourceId='com.instagram.android:id/row_feed_view_all_comments_text')
        if comment_section.exists:
            comment_section.click()
            random_sleep(3, 4)
            logging.info("Opened comment section")
            return Response({'status': 'success', 'message': 'Opened comment section'})
        else:
            logging.info("Comment section not found")
            return Response({'status': 'warning', 'message': 'Comment section not found'}, status=404)
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for closing the comment section
@api_view(['GET'])
def close_comment_section_view(request):
    try:
        d.press.back()
        logging.info("Closed comment section.")
        return Response({'status': 'success', 'message': 'Closed comment section'})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for checking if in the comment section
@api_view(['GET'])
def is_in_comment_section_view(request):
    try:
        in_section = d.exists(resourceId='com.instagram.android:id/layout_comment_thread_edittext')
        return Response({'in_comment_section': in_section})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)


# DRF view for getting comments with specific keywords
@api_view(['GET'])
def get_comments_with_keywords_view(request):
    try:
        keywords = request.GET.get('keywords', '').split(',')
        batches = int(request.GET.get('batches', 2))
        all_comments = set()
        extracted_comments = []

        for _ in range(batches):
            comment_elements = d(resourceId='com.instagram.android:id/row_comment_textview_comment')
            for comment_element in comment_elements:
                comment_text = comment_element.text
                if comment_text not in all_comments and any(keyword in comment_text for keyword in keywords):
                    all_comments.add(comment_text)
                    extracted_comments.append(comment_text)

            d.swipe(500, 1000, 500, 500, steps=10)
            random_sleep(1, 2)

        return Response({'extracted_comments': extracted_comments})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for capturing comments
@api_view(['GET'])
def capture_comments_view(request):
    try:
        batches = int(request.GET.get('batches', 1))
        max_likes = request.GET.get('max_likes')
        max_likes = int(max_likes) if max_likes else None
        liked_count = 0
        all_comments = []
        previous_comments = set()
        repetitive_count = 0

        for _ in range(batches):
            comments = []
            comment_elements = d(resourceId='com.instagram.android:id/row_comment_textview_comment')
            for element in comment_elements:
                comment_text = element.text
                if comment_text not in previous_comments:
                    comments.append(comment_text)
                    previous_comments.add(comment_text)

            all_comments.extend(comments)

            # Check if comments are repetitive and break if they are
            if len(set(comments)) == len(previous_comments):
                repetitive_count += 1
                if repetitive_count >= 2:
                    break
            else:
                repetitive_count = 0

            # Swipe logic, assuming swiping brings new comments
            d.swipe(500, 1165, 515, 680, steps=30)
            random_sleep(1, 2)

        return Response({'captured_comments': all_comments, 'liked_count': liked_count})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

@api_view(['POST'])
def like_comments_based_on_criteria_view(request):
    try:
        data = json.loads(request.body)
        comments = data.get('comments', [])
        liked_count = int(data.get('liked_count', 0))
        max_likes = int(data.get('max_likes', 0))

        keywords = ["😊", "👍", "❤️", "🥰", "😘", "😍", "🤤"]

        for comment in comments:
            if liked_count >= max_likes:
                break
            if any(keyword in comment['text'] for keyword in keywords):
                success = like_comment(comment)
                if success:
                    liked_count += 1

        logging.info(f"Liked {liked_count} comments based on criteria.")
        return Response({'liked_count': liked_count})
    except Exception as e:
        logging.error(str(e))
        return Response({'status': 'error', 'message': str(e)}, status=500)

def like_comment(comment):
    try:
        all_comment_elements = d(resourceId='com.instagram.android:id/row_comment_textview_comment')
        all_like_buttons = d(resourceId='com.instagram.android:id/row_comment_like_button_click_area')
        # Assuming comment contains an index or some identifier to find the correct element
        comment_index = comment['index']
        like_button = all_like_buttons[comment_index]
        like_button.click()
        logging.info(f"Successfully liked the comment: '{comment['text']}'.")
        return True
    except Exception as e:
        logging.error(f"Error liking the comment: '{comment['text']}'. {str(e)}")
        return False
