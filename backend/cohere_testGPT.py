import os
import re
import cohere
from dotenv import load_dotenv

# Load API key on module load
load_dotenv()
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

asked_questions = set()  # Use session-based tracking for web

def generate_question(level):
    """Generate a STEM question using Cohere API."""
    prompt = f"""
Generate a level {level} real-world STEM multiple choice question (difficulty increases with level).
Format:
Question: [question]
a) [option]
b) [option]
c) [option]
d) [option]
Answer: [a/b/c/d]
Reason: [one sentence explanation]
"""

    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
    )

    return response.generations[0].text.strip()

def parse_response(response_text):
    """Parse question, options, correct answer, and reason from text."""
    q = re.search(r'Question:\s*(.*?)(?=\n[a-d]\)|\na\))', response_text, re.DOTALL)
    question = q.group(1).strip() if q else "Unclear question"

    patterns = [
        r'a\)\s*(.*?)(?=\nb\)|$)',
        r'b\)\s*(.*?)(?=\nc\)|$)',
        r'c\)\s*(.*?)(?=\nd\)|$)',
        r'd\)\s*(.*?)(?=\nAnswer:|$)'
    ]
    options = [re.search(p, response_text, re.DOTALL).group(1).strip() if re.search(p, response_text, re.DOTALL) else "" for p in patterns]

    a = re.search(r'Answer:\s*([a-dA-D])', response_text)
    answer = a.group(1).lower() if a else 'a'

    r = re.search(r'Reason:\s*(.*?)(?=\n\n|$)', response_text, re.DOTALL)
    reason = r.group(1).strip() if r else "No reason provided"

    return question, options, answer, reason

def get_unique_question(level):
    """Ensure no duplicate questions."""
    for _ in range(5):
        raw = generate_question(level)
        question, options, answer, reason = parse_response(raw)
        if question not in asked_questions:
            asked_questions.add(question)
            return {
                "question": question,
                "options": options,
                "answer": answer,
                "reason": reason
            }
    return None
