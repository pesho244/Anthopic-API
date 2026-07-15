from multi_turn import add_user_message, chat
from prompt_evaluator import PromptEvaluator

# Increase max_concurrent_tasks for greater concurrency, but beware of rate limit errors!
evaluator = PromptEvaluator(max_concurrent_tasks=1)

dataset = evaluator.generate_dataset(
    # Describe the purpose or goal of the prompt you're trying to test
    task_description="Write a compact, concise 1 day meal plan for a single athlete",
    # Describe the different inputs that your prompt requires
    prompt_inputs_spec={
        "height": "Athlete's height in cm",
        "weight": "Athlete's weight in kg",
        "goal": "Goal of the athlete",
        "restrictions": "Dietary restrictions of the athlete",
    },
    # Where to write the generated dataset
    output_file="dataset.json",
    # Number of test cases to generate (keep this low if you're getting rate limit errors)
    num_cases=1,
)


def run_prompt(prompt_inputs):
    """Define and run the prompt you want to evaluate, returning the raw model output.
    This function is executed once for each test case"""
    prompt = f"""
    Generate a one-day meal plan for an athlete that meets their dietary restrictions.

    <athlete_information>
    - Height: {prompt_inputs["height"]}
    - Weight: {prompt_inputs["weight"]}
    - Goal: {prompt_inputs["goal"]}
    - Dietary restrictions: {prompt_inputs["restrictions"]}
    </athlete_information>

    Guidelines:
    1. Include accurate daily calorie amount
    2. Show protein, fat, and carb amounts
    3. Specify when to eat each meal
    4. Use only foods that fit restrictions
    5. List all portion sizes in grams
    6. Keep budget-friendly if mentioned
    """

    messages = []
    add_user_message(messages, prompt)
    return chat(messages)


if __name__ == "__main__":
    results = evaluator.run_evaluation(
        run_prompt_function=run_prompt,
        dataset_file="dataset.json",
        extra_criteria="""
        The output should include:
        - Daily caloric total
        - Macronutrient breakdown
        - Meals with exact foods, portions, and timing
        """,
    )