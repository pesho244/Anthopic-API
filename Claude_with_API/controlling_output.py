from multi_turn import add_user_message, add_assistant_message, chat

messages = []

add_user_message(messages, "Generate a very short event bridge rule as json, very short answer")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])

print(text)