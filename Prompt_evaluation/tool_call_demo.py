from multi_turn import add_user_message, chat
from tools import get_current_datetime_schema

messages = []
add_user_message(messages, "What is the exact time, formatted as HH:MM:SS?")

response = chat(messages, tools=[get_current_datetime_schema])

# Inspect the response - this is no longer a single text block.
# It's a LIST of content blocks, which may include a text block
# AND a tool_use block together.
print(response.content)
print("\nstop_reason:", response.stop_reason)

for block in response.content:
    if block.type == "text":
        print("\n[Text block]:", block.text)
    elif block.type == "tool_use":
        print("\n[Tool use block]")
        print("  id:", block.id)
        print("  name:", block.name)
        print("  input:", block.input)