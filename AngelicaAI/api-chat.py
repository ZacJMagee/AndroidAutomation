from textgen_messaging import TextgenMessaging
from supabase_handler import SupabaseHandler
import asyncio


async def get_response_from_textgenai(user_input, history):
    messaging = TextgenMessaging()
    return messaging.send_message_and_get_response(user_input, history)


async def save_chat_history(user_id, user_input, response_text, history):
    history_data = {
        'user_id': user_id,
        'history': {
            'internal': history.get('internal', []) + [[user_input, response_text]],
            'visible': history.get('visible', []) + [[user_input, response_text]]
        }
    }
    await SupabaseHandler.save_chat_history(user_id, history_data)
    return history_data


async def main():
    user_id = input("Enter User ID: ")  # Dynamic user ID input
    user_input = input("You: ")

    history_data = await SupabaseHandler.get_chat_history(user_id) or {}
    history = history_data.get('history', {'internal': [], 'visible': []})

    response_text = await get_response_from_textgenai(user_input, history)
    updated_history = await save_chat_history(user_id, user_input, response_text, history)

    print(f"TextgenAI: {updated_history['history']['visible'][-1][1]}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        SupabaseHandler.close()
