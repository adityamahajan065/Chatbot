# main.py
from chatbot import WikiBot

def run_bot():
    bot = WikiBot()
    bot.greet()

    while True:
        user_input = input("\nYou: ")
        response = bot.handle_input(user_input)
        if response == "exit":
            print("\nSmartBot: Goodbye!")
            break
        else:
            print(f"\nSmartBot: {response}")

if __name__ == "__main__":
    run_bot()
