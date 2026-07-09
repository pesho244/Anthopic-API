from multi_turn import client, add_user_message, add_assistant_message

# --- Step 1: Draft a Prompt ---
# This is the "version 1" prompt we want to test and later improve.
def build_prompt(question):
    return f"""
Please answer the user's question:

{question}
Answer the question with simple detail
"""


# --- Step 2: Create an Eval Dataset ---
# Sample questions representing the kinds of things real users will ask.
eval_dataset = [
    "What's 2+2?",
    "How do I make oatmeal?",
    "How far away is the Moon?",
]


# --- Step 3: Feed Through Claude ---
def get_answer(question):
    prompt = build_prompt(question)
    messages = [{"role": "user", "content": prompt}]
    return chat(messages)


# --- Step 4: Feed Through a Grader ---
# We use Claude itself as the grader, asking it to score the answer 1-10.
def grade_answer(question, answer):
    grading_prompt = f"""
You are grading the quality of an AI assistant's answer.

Question: {question}
Answer: {answer}

Score the answer from 1 to 10, where 10 is a perfect, complete, helpful answer
and 1 is a poor or unhelpful answer.

Respond with ONLY the number, nothing else.
"""
    messages = [{"role": "user", "content": grading_prompt}]
    result = chat(messages, temperature=0)
    try:
        return float(result.strip())
    except ValueError:
        print(f"Could not parse grader output: {result!r}")
        return 0


# --- Step 5: Run the full eval and print an average score ---
def run_eval(label="Prompt version"):
    scores = []
    print(f"\n=== {label} ===")
    for question in eval_dataset:
        answer = get_answer(question)
        score = grade_answer(question, answer)
        scores.append(score)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print(f"Score: {score}/10\n")

    average = sum(scores) / len(scores)
    print(f"Average score for '{label}': {average:.2f}/10")
    return average


if __name__ == "__main__":
    run_eval("Baseline prompt")

    # --- To test an improved prompt version ---
    # Update build_prompt() above to add more instructions, e.g.:
    #
    # def build_prompt(question):
    #     return f"""
    # Please answer the user's question:
    #
    # {question}
    #
    # Answer the question with ample detail
    # """
    #
    # Then re-run this file and compare the new average score to the baseline.