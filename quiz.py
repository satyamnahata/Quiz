import json
import os
import random

quizzes_file = "quizzes.json"
scores_file = "scores.json"

# Load quizzes
if os.path.exists(quizzes_file):
    with open(quizzes_file, "r") as f:
        quizzes = json.load(f)
else:
    quizzes = {}

# Main Menu
print("\nWelcome to Satyam's No-Def Quiz Game 🤓")
print("1. Create a quiz")
print("2. Play a quiz")
print("3. View leaderboard")
choice = input("Choose (1/2/3): ")

# ---------- Create a Quiz ----------
if choice == '1':
    topic = input("Enter quiz topic: ").strip()
    questions = []

    while True:
        question = input("\nEnter a question: ").strip()
        options = []
        for i in range(4):
            option = input(f"Option {chr(97+i)}: ")  # a, b, c, d
            options.append(option)
        answer = input("Correct option (a/b/c/d): ").lower()
        questions.append({
            "question": question,
            "options": options,
            "answer": answer
        })

        more = input("Add another question? (y/n): ").lower()
        if more != 'y':
            break

    quizzes[topic] = questions

    with open(quizzes_file, "w") as f:
        json.dump(quizzes, f, indent=4)

    print(f"Quiz '{topic}' saved successfully!")

# ---------- Play a Quiz ----------
elif choice == '2':
    if not quizzes:
        print("No quizzes available.")
    else:
        print("\nAvailable topics:")
        for i, topic in enumerate(quizzes):
            print(f"{i + 1}. {topic}")
        topic_index = int(input("Pick a topic number: ")) - 1
        topic_name = list(quizzes.keys())[topic_index]

        selected_questions = quizzes[topic_name]
        random.shuffle(selected_questions)

        score = 0
        for q in selected_questions:
            print(f"\n{q['question']}")
            for i, opt in enumerate(q["options"]):
                print(f"{chr(97+i)}) {opt}")
            user_ans = input("Your answer: ").lower()

            if user_ans == q["answer"]:
                print("Correct ✅")
                score += 1
            else:
                print(f"Wrong ❌ (Correct: {q['answer']})")

        print(f"\nFinal Score: {score}/{len(selected_questions)}")

        # Save score
        name = input("Enter your name: ")
        if os.path.exists(scores_file):
            with open(scores_file, "r") as f:
                scores = json.load(f)
        else:
            scores = []

        scores.append({
            "name": name,
            "topic": topic_name,
            "score": score
        })

        with open(scores_file, "w") as f:
            json.dump(scores, f, indent=4)

# ---------- View Leaderboard ----------
elif choice == '3':
    if os.path.exists(scores_file):
        with open(scores_file, "r") as f:
            scores = json.load(f)

        print("\n🏆 Leaderboard (Top 5):")
        sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]
        for i, entry in enumerate(sorted_scores):
            print(f"{i+1}. {entry['name']} - {entry['score']} pts on '{entry['topic']}'")
    else:
        print("No scores found yet.")
else:
    print("Invalid choice.")
