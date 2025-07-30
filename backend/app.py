from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import cohere
from dotenv import load_dotenv
import random

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# User state tracking (for demo, we assume one user)
user_state = {
    "level": 1,
    "stars": 0,
    "history": [],
    "previous_question": None,
    "used_questions": set()
}


def generate_question(level):
    """Generate a new question using Cohere."""
    prompt = f"Generate a level {level} STEM question with options in the following format:\n" \
             f"Question: [Generated question]\n" \
             f"a) [Option A]\n" \
             f"b) [Option B]\n" \
             f"c) [Option C]\n" \
             f"d) [Option D]\n" \
             f"Answer: [a/b/c/d]\n" \
             f"Reason: [One sentence explanation for that answer]"

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=300,
        temperature=0.8,
    )
    return response.generations[0].text.strip()


def parse_response(text):
    """Parse Cohere output into structured components."""
    question_match = re.search(r'Question:\s*(.*?)(?=\n[a-d]\)|\na\))', text, re.DOTALL)
    question = question_match.group(1).strip() if question_match else "Could not parse question"

    options = []
    option_patterns = [
        r'a\)\s*(.*?)(?=\nb\)|$)',
        r'b\)\s*(.*?)(?=\nc\)|$)',
        r'c\)\s*(.*?)(?=\nd\)|$)',
        r'd\)\s*(.*?)(?=\nAnswer:|$)'
    ]
    for pattern in option_patterns:
        match = re.search(pattern, text, re.DOTALL)
        options.append(match.group(1).strip() if match else "Option missing")

    answer_match = re.search(r'Answer:\s*([a-dA-D])', text)
    correct = answer_match.group(1).lower() if answer_match else 'a'

    reason_match = re.search(r'Reason:\s*(.*?)(?=\n\n|$)', text, re.DOTALL)
    reason = reason_match.group(1).strip() if reason_match else "No reason provided"

    return question, options, correct, reason


@app.route("/api/state")
def get_state():
    return jsonify({
        "level": user_state["level"],
        "stars": user_state["stars"]
    })


@app.route("/api/question")
def get_question():
    for _ in range(5):  # try a few times to avoid repeats
        raw = generate_question(user_state["level"])
        question, options, correct, reason = parse_response(raw)
        question_key = question.lower().strip()

        if question_key not in user_state["used_questions"]:
            user_state["used_questions"].add(question_key)
            user_state["previous_question"] = {
                "question": question,
                "options": options,
                "correct": correct,
                "reason": reason
            }
            return jsonify(user_state["previous_question"])

    # Fallback in case all retries repeat
    return jsonify(user_state["previous_question"])
@app.route("/api/suggestion")
def career_suggestion():
    history = user_state.get("history", [])
    level = user_state.get("level", 1)

    if not history:
        return jsonify({"message": "Not enough data to suggest a career yet."})

    total_time = sum(item.get("time_taken", 0) for item in history)
    avg_time = total_time / len(history)

    correct_answers = sum(1 for item in history if item["answer"] == item["correct"])
    accuracy = correct_answers / len(history)

    # Classify speed
    if avg_time <= 15:
        speed = "fast thinker"
    elif avg_time <= 30:
        speed = "balanced thinker"
    else:
        speed = "deep thinker"

    # Suggestion logic
    suggestion = "Science Enthusiast"
    if level <= 2:
        suggestion = "School-level Explorer: Science Communicator, STEM Mentor"
    elif level <= 4:
        if accuracy > 0.7 and speed != "deep thinker":
            suggestion = "Engineer (Mechanical, Civil, Electrical)"
        else:
            suggestion = "Lab Technician or Research Assistant"
    elif level <= 6:
        if accuracy > 0.8 and speed == "fast thinker":
            suggestion = "Robotics Engineer or Data Scientist"
        else:
            suggestion = "Environmental Scientist or Physicist"
    else:
        if accuracy > 0.9:
            suggestion = "AI Scientist or Astronomer"
        else:
            suggestion = "University Professor or Research Director"

    return jsonify({
        "level": level,
        "accuracy": round(accuracy * 100, 2),
        "average_time": round(avg_time, 2),
        "speed_type": speed,
        "career_suggestion": suggestion
    })



@app.route("/api/submit", methods=["POST"])
def submit_answer():
    try:
        data = request.json
        user_answer = data.get("user_answer")
        correct_answer = data.get("correct_answer")
        time_taken = data.get("time_taken", 0)

        if not user_state.get("previous_question"):
            return jsonify({"error": "No previous question."}), 400

        user_state["history"].append({
            "question": user_state["previous_question"],
            "answer": user_answer,
            "correct": correct_answer,
            "time_taken": time_taken
        })

        if user_answer == correct_answer:
            user_state["stars"] += 1
            if user_state["stars"] >= 10:
                user_state["level"] += 1
                user_state["stars"] = 0
                return jsonify({"result": "level_up", "level": user_state["level"]})
            return jsonify({"result": "correct"})
        else:
            return jsonify({"result": "wrong", "reason": user_state["previous_question"]["reason"]})

    except Exception as e:
        print("Submit error:", e)
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)