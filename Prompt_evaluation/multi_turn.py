from dotenv import load_dotenv
load_dotenv()
import anthropic
from anthropic.types import Message

client = anthropic.Anthropic()
model = "claude-sonnet-4-5"


def add_user_message(messages, message):
    # 'message' can be a plain string, a list of blocks (e.g. tool_result
    # blocks), or a full Message object returned by chat()
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


def text_from_message(message):
    """Extracts and joins all text blocks from a full Message object,
    useful for displaying Claude's final answer to the user."""
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )


def chat(messages, system=None, temperature=1.0, stop_sequences=None, tools=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }

    if system:
        params["system"] = system

    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    if tools:
        params["tools"] = tools

    message = client.messages.create(**params)
    return message