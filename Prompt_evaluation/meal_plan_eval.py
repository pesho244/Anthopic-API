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

    Here is an example input with an ideal response:

    <sample_input>
    - Height: 175cm
    - Weight: 70kg
    - Goal: Muscle gain
    - Dietary restrictions: Vegetarian
    </sample_input>

    <ideal_output>
    Daily Calories: 2800 kcal
    Macros: Protein 160g, Fat 80g, Carbs 340g

    7:00 AM - Breakfast: Oats (100g), Greek yogurt (200g), banana (120g)
    12:00 PM - Lunch: Lentils (150g dry), rice (200g cooked), spinach (100g)
    3:00 PM - Snack: Cottage cheese (150g), almonds (30g)
    7:00 PM - Dinner: Tofu (200g), quinoa (150g cooked), broccoli (150g)
    </ideal_output>

    This example is well-structured, provides exact gram-based portions,
    clear meal timing, and hits the muscle-gain macro targets while
    strictly respecting the vegetarian restriction.

    Now generate a similar meal plan for the athlete information given above.
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