import os
import cohere
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key=cohere_api_key)

def generate_question(prompt):
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
    )
    return response.generations[0].text  # Updated line

