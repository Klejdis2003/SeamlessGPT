from gpt import Nemotron

instruction = "Enter :q to quit the chat."


def chat():
    print(instruction)
    gpt = Nemotron()
    while True:
        user_input = input("You: ")
        if user_input == ":q":
            print("Chat ended.")
            break

        response = gpt.send_message(message=user_input, with_previous_chat_context=True, remember_response=True)
        print(f"Bot: {response}")


if __name__ == '__main__':
    chat()
