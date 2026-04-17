from .chatbot import Chatbot


def main():
    bot = Chatbot()
    print("Chatbot starter. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        print("Bot:", bot.respond(user_input))


if __name__ == "__main__":
    main()
