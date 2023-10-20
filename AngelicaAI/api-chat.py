from textgen_messaging import TextgenMessaging
from supabase_handler import SupabaseHandler
import asyncio


async def chat_with_textgenai(user_input, user_id, history):
    messaging = TextgenMessaging()
    response_text = messaging.send_message_and_get_response(
        user_input, history)

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
    user_id = "123456"
    user_input = input("You: ")

    history_data = await SupabaseHandler.get_chat_history(user_id) or {}
    history = history_data.get('history', {'internal': [], 'visible': []})

    history = await chat_with_textgenai(user_input, user_id, history)
    print(f"TextgenAI: {history['history']['visible'][-1][1]}")

if __name__ == "__main__":
    asyncio.run(main())

SupabaseHandler.close()
