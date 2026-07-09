from dotenv import load_dotenv
load_dotenv()
import anthropic

client = anthropic.Anthropic()
model = "claude-sonnet-4-5"

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages, system=None, temperature=1.0, stop_sequences=None):
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

    message = client.messages.create(**params)
    return message.content[0].text

# --- Putting it all together ---

if __name__ == "__main__":
    messages = []

    system = """
    You are a senior QA automation engineer.
    Guide the user to a solution step by step.
    Always answer in exactly one sentence.
    """

    add_user_message(messages, "How to figure out what design patterns to use for Automation testing?")

    answer = chat(messages, system=system)

    print(answer)