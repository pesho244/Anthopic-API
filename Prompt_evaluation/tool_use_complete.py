from multi_turn import add_user_message, add_assistant_message, chat, text_from_message
from tools import (
    get_current_datetime,
    get_current_datetime_schema,
    add_duration_to_datetime,
    add_duration_to_datetime_schema,
    set_reminder,
    set_reminder_schema,
)

# Maps a tool's name (as Claude sees it) to the real Python function to run
available_tools = {
    "get_current_datetime": get_current_datetime,
    "add_duration_to_datetime": add_duration_to_datetime,
    "set_reminder": set_reminder,
}

tool_schemas = [
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema,
]


def run_tool(tool_use_block):
    """Executes the real function that corresponds to one ToolUse block"""
    tool_name = tool_use_block.name
    tool_input = tool_use_block.input

    function = available_tools[tool_name]

    try:
        result = function(**tool_input)
        is_error = False
    except Exception as e:
        result = str(e)
        is_error = True

    return {
        "type": "tool_result",
        "tool_use_id": tool_use_block.id,
        "content": str(result),
        "is_error": is_error,
    }


def run_conversation(user_input):
    messages = []
    add_user_message(messages, user_input)

    while True:
        response = chat(messages, tools=tool_schemas)
        add_assistant_message(messages, response)

        # Print any text Claude included alongside its tool request(s)
        text = text_from_message(response)
        if text:
            print("Claude:", text)

        # If Claude didn't ask for any tools, we're done - print final answer
        if response.stop_reason != "tool_use":
            break

        # Claude may request one OR multiple tool calls in a single response.
        # Run each one and collect its result.
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"\n[Running tool: {block.name}({block.input})]")
                tool_results.append(run_tool(block))

        # Send all tool results back as a single user message
        add_user_message(messages, tool_results)

    return messages


if __name__ == "__main__":
    run_conversation("What is the exact time, formatted as HH:MM:SS?")