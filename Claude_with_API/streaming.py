from multi_turn import add_user_message
from dotenv import load_dotenv
load_dotenv()
import anthropic

client = anthropic.Anthropic()
model = "claude-sonnet-4-5"
messages = []
add_user_message(messages, "Write a 1 sentence description of a fake database")

with client.messages.stream(
        model=model,
        max_tokens=1000,
        messages=messages
) as stream:
    for text in stream.text_stream:
        # Send each chunk to your client
        pass

    # Get the complete message for database storage
    final_message = stream.get_final_message()