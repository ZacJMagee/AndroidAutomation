from rest_framework.decorators import api_view
from rest_framework.response import Response
from uiautomator import device as d
import logging
import re
import json

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# DRF view for opening messages in Instagram
@api_view(['GET'])
def open_messages_view(request):
    try:
        inbox_button = d(resourceId="com.instagram.android:id/action_bar_inbox_button")
        if inbox_button.wait.exists(timeout=10000):
            content_desc = inbox_button.info.get('contentDescription', '')
            match = re.search(r'(\d+) unread message', content_desc)
            num_unread_messages = int(match.group(1)) if match else 0
            inbox_button.click()
            return Response({'status': 'success', 'num_unread_messages': num_unread_messages})
        else:
            return Response({'status': 'error', 'message': 'Inbox button not found'}, status=404)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for listing new messages
@api_view(['GET'])
def list_new_messages_view(request):
    try:
        usernames_with_new_messages = []
        chat_containers = d(resourceId="com.instagram.android:id/row_inbox_container")
        if not chat_containers.wait.exists(timeout=10000):
            return Response({'status': 'error', 'message': 'Chat containers not found'}, status=404)

        for chat_container in chat_containers:
            username_element = chat_container.child(resourceId="com.instagram.android:id/row_inbox_username")
            if username_element.wait.exists(timeout=10000):
                content_desc = chat_container.info.get('contentDescription', '')
                if 'unread' in content_desc:
                    usernames_with_new_messages.append(username_element.text)

        return Response({'status': 'success', 'usernames_with_new_messages': usernames_with_new_messages})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)


# DRF view for opening a specific chat
@api_view(['POST'])
def open_specific_chat_view(request):
    try:
        username = request.data.get('username')
        chat_element = d(resourceId="com.instagram.android:id/row_inbox_container",
                         descriptionMatches=f"^{username},.*")
        if chat_element.exists:
            chat_element.click()
            return Response({'status': 'success', 'message': f"Opened chat with {username}"})
        else:
            return Response({'status': 'warning', 'message': f"Chat element for {username} not found"}, status=404)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for getting the username in a chat
@api_view(['GET'])
def get_username_view(request):
    try:
        username = d(resourceId="com.instagram.android:id/row_thread_title_textview").text
        return Response({'username': username})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for getting the last message from a chat
@api_view(['POST'])
def get_last_message_view(request):
    try:
        username = request.data.get('username')
        message_elements = d(resourceId="com.instagram.android:id/direct_text_message_text_view")
        if message_elements.exists:
            last_message = message_elements[-1].text
            return Response({'last_message': last_message})
        else:
            return Response({'status': 'warning', 'message': f"No messages found in the chat with {username}"}, status=404)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for sending a message in a chat
@api_view(['POST'])
def send_message_view(request):
    try:
        message = request.data.get('message')
        text_field = d(resourceId="com.instagram.android:id/row_thread_composer_edittext")
        if text_field.exists:
            text_field.set_text(message)
            send_button = d(resourceId="com.instagram.android:id/row_thread_composer_button_send")
            if send_button.exists:
                send_button.click()
                return Response({'status': 'success', 'message': 'Message sent'})
            else:
                return Response({'status': 'warning', 'message': 'Send button not found'}, status=404)
        else:
            return Response({'status': 'warning', 'message': 'Text input field not found'}, status=404)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for responding to the last message in a chat
@api_view(['POST'])
def respond_to_last_message_view(request):
    try:
        messages = request.data.get('messages')
        response = textgen_messaging.send_message(messages[-1], messages)  # Assuming textgen_messaging is accessible
        send_message(response)
        return Response({'status': 'success', 'response': response})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)


# DRF view for fetching the latest chat history
@api_view(['GET'])
def fetch_latest_chat_history_view(request):
    try:
        username = request.GET.get('username')
        chat_history = supabase_handler.get_chat_history(username)  # Ensure supabase_handler is accessible
        return Response({'chat_history': chat_history})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for storing a message
@api_view(['POST'])
def store_message_view(request):
    try:
        data = request.data
        conversation_id = data.get('conversation_id')
        message_text = data.get('message_text')
        timestamp = data.get('timestamp')
        sender = data.get('sender')
        supabase_handler.store_message(conversation_id, message_text, timestamp, sender)  # Ensure supabase_handler is accessible
        return Response({'status': 'success', 'message': 'Message stored'})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for getting recent messages
@api_view(['GET'])
def get_recent_messages_view(request):
    try:
        conversation_id = request.GET.get('conversation_id')
        limit = int(request.GET.get('limit', 10))
        recent_messages = supabase_handler.get_recent_messages(conversation_id, limit)  # Ensure supabase_handler is accessible
        return Response({'recent_messages': recent_messages})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)

# DRF view for closing a chat
@api_view(['GET'])
def close_chat_view(request):
    try:
        back_button = d(resourceId="com.instagram.android:id/action_bar_button_back")
        if back_button.exists:
            back_button.click()
            return Response({'status': 'success', 'message': 'Chat closed'})
        else:
            return Response({'status': 'warning', 'message': 'Back button not found'}, status=404)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)
