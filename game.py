import os
import re
import cohere
from dotenv import load_dotenv

def generate_question(co, level):
    """Generate a STEM question using Cohere API."""
    prompt = f"Generate a unique level {level} STEM question with options to test student understanding in science, technology, engineering, mathematics in the following format:\n" \
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
        temperature=0.7,
    )
    
    return response.generations[0].text

def parse_response(response_text):
    """Parse the response from Cohere API to extract question, options, answer, and reason."""
    # Extract question
    question_match = re.search(r'Question:\s*(.*?)(?=\n[a-d]\)|\na\))', response_text, re.DOTALL)
    question = question_match.group(1).strip() if question_match else "Could not parse question"
    
    # Extract options
    options = []
    option_patterns = [
        r'a\)\s*(.*?)(?=\nb\)|$)',
        r'b\)\s*(.*?)(?=\nc\)|$)',
        r'c\)\s*(.*?)(?=\nd\)|$)',
        r'd\)\s*(.*?)(?=\nAnswer:|$)'
    ]
    
    for pattern in option_patterns:
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            options.append(match.group(1).strip())
        else:
            options.append("Option not provided")
    
    # Extract answer
    answer_match = re.search(r'Answer:\s*([a-dA-D])', response_text)
    if answer_match:
        answer = answer_match.group(1).lower()
    else:
        raise ValueError("Could not parse the correct answer from the response.")
    
    # Extract reason
    reason_match = re.search(r'Reason:\s*(.*?)(?=\n\n|$)', response_text, re.DOTALL)
    reason = reason_match.group(1).strip() if reason_match else "No explanation provided"
    
    return question, options[:4], answer, reason

def display_question(question, options):
    """Display the question and options in a clear format."""
    print(f"\n{question}")
    for i, opt in enumerate(options):
        print(f"{chr(97 + i)}) {opt}")

def main():
    print("Welcome to STEM Master!")
    level = 1
    stars = 0
    
    # Load environment variables
    load_dotenv()
    
    # Initialize Cohere client
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        print("Error: COHERE_API_KEY not found in .env file")
        return
    
    co = cohere.Client(cohere_api_key)

    while True:
        print(f"\nLevel {level} | Stars: {stars}")
        
        # Generate question
        raw_response = generate_question(co, level)
        
        # Parse response
        try:
            question, options, answer, reason = parse_response(raw_response)
            
            # Display only the question and options (not the answer or reason)
            display_question(question, options)
            
            # Get user input and validate answer
            user_answer = input("\nYour answer (a/b/c/d): ").strip().lower()
            while user_answer not in ['a', 'b', 'c', 'd']:
                print("Invalid input. Please enter a/b/c/d.")
                user_answer = input("Your answer (a/b/c/d): ").strip().lower()
            
            # Check answer and provide appropriate feedback
            if user_answer == answer:
                print(f"You got the correct answer!")
                stars += 1
                if stars >= 10:
                    level += 1
                    stars = 0
                    print("\nCongratulations! You've leveled up!")
            else:
                print(f"Wrong! The correct answer is {answer}. Reason: {reason}")
            
        except Exception as e:
            print(f"Error processing question: {e}")
            continue

if __name__ == "__main__":
    main()