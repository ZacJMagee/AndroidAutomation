from Instagram.instaChatbot import InstagramChatbot

print("Starting script...")


def main():
    # Create an instance of InstagramChatbot
    chatbot = InstagramChatbot()
    print("InstagramChatbot initialized")

    # List all available chats (usernames)
    chatbot.list_usernames()
    print("Listed names")

    # Open chat with Molly
    chatbot.open_specific_chat("molly magee ˙ᵕ˙")
    print("Opened chat with Molly.")

    # Get the last two messages from the chat
    messages = chatbot.read_messages_last_two()
    print(f"Retrieved last two messages: {messages}")

    # Fetch the latest chat history from Supabase
    latest_history = chatbot.fetch_latest_chat_history("molly magee ˙ᵕ˙")
    print(f"Retrieved latest history from Supabase: {latest_history}")

    # Generate a response using the last two messages
    response = chatbot.respond_to_last_message(messages)
    print(f"Generated response: {response}")

    # Send the generated response to Molly
    chatbot.send_message(response)
    print("Response sent to Molly's chat.")

    # Store the last two messages to Supabase
    chatbot.store_messages(messages)
    print(f"Stored {len(messages)} messages to Supabase.")

    print("Script stopped.")


# Run the main method
main()
