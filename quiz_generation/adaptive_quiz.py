import json
import os

def load_quiz_results(filepath="quiz_results.json"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {}

def save_quiz_results(results, filepath="quiz_results.json"):
    with open(filepath, "w") as f:
        json.dump(results, f, indent=2)

def present_question(question_obj):
    print("\nQuestion:")
    print(question_obj["question"])
    for option in question_obj["options"]:
        print(option)
    answer = input("Your answer (enter the option letter): ").strip().upper()
    return answer

def evaluate_answer(question_obj, user_answer):
    correct = user_answer == question_obj["correct_answer"]
    if correct:
        print("Correct!")
    else:
        print(f"Incorrect. The correct answer is {question_obj['correct_answer']}.")
    return correct

def generate_follow_up(question):
    """
    For demonstration, this function simulates calling an LLM to generate
    an explanation and a new question for a given topic.
    In practice, you would integrate your LLM call here.
    """
    explanation = (
        f"Explanation for {question.get('topic', 'the topic')}: Remember that photosynthesis "
        "involves light energy converting CO2 and water into glucose."
    )
    new_question = {
        "question": "What is the primary purpose of photosynthesis?",
        "options": [
            "A. Produce oxygen",
            "B. Produce glucose",
            "C. Produce water",
            "D. Produce carbon dioxide"
        ],
        "correct_answer": "B",
        "topic": question.get("topic", "General")
    }
    return {"explanation": explanation, "question": new_question}

def run_quiz(quiz):
    results = load_quiz_results()
    for idx, question in enumerate(quiz):
        print(f"\n--- Question {idx+1} ---")
        user_answer = present_question(question)
        is_correct = evaluate_answer(question, user_answer)
        # Log result for tracking:
        results[f"question_{idx+1}"] = {
            "topic": question.get("topic", "General"),
            "user_answer": user_answer,
            "correct_answer": question["correct_answer"],
            "is_correct": is_correct
        }
        # Adaptive follow-up if answer is incorrect:
        if not is_correct:
            follow_up = generate_follow_up(question)
            print("\nFollow-Up Explanation:")
            print(follow_up["explanation"])
            # Optionally, re-ask with the new question:
            print("\nRe-Quiz Question:")
            new_answer = present_question(follow_up["question"])
            is_retry_correct = evaluate_answer(follow_up["question"], new_answer)
            results[f"question_{idx+1}_retry"] = {
                "user_answer": new_answer,
                "correct_answer": follow_up["question"]["correct_answer"],
                "is_correct": is_retry_correct
            }
    save_quiz_results(results)
    print("\nQuiz completed. Your results have been saved.")

if __name__ == "__main__":
    # For testing, use a sample quiz containing two questions
    sample_quiz = [
        {
            "question": "What is the process by which plants convert sunlight into energy?",
            "options": [
                "A. Respiration",
                "B. Photosynthesis",
                "C. Transpiration",
                "D. Fermentation"
            ],
            "correct_answer": "B",
            "topic": "Photosynthesis"
        },
        {
            "question": "Which gas is released during photosynthesis?",
            "options": [
                "A. Oxygen",
                "B. Carbon Dioxide",
                "C. Nitrogen",
                "D. Hydrogen"
            ],
            "correct_answer": "A",
            "topic": "Photosynthesis"
        }
    ]
    run_quiz(sample_quiz) 

