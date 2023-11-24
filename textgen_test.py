from AngelicaAI.textgen_messaging import TextgenMessaging

def main():
    textgen = TextgenMessaging()
    user_input = "Hello, how are you?"
    history = []
    response = textgen.send_message(user_input, history)
    print(response)

if __name__ == "__main__":
    main()
