from textgen_messaging import TextgenMessaging


def chat_with_textgenai(user_input, user_id, history):
    messaging = TextgenMessaging()

    # Send the user input to TextgenAI and get a response
    response = messaging.send_message_and_get_response(user_input, history)

    # Append the user's message to the history
    history['visible'].append({"role": "user", "content": user_input})

    # Append the LLM's response to the history
    history['visible'].append({"role": "TextgenAI", "content": response})

    # Save the updated chat history to the Supabase database
    messaging.save_chat_history(user_id, history)

    return history


if __name__ == "__main__":
    user_id = "example_user_id"  # This can be any unique identifier for the user
    history = {'internal': [], 'visible': []}  # Initialize the chat history

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        history = chat_with_textgenai(user_input, user_id, history)

        # Print the LLM's response
        # Get the latest message from the history
        latest_response = history['visible'][-1]['content']
        print(f"TextgenAI: {latest_response}")
