import os
import cohere
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize Cohere client
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        print("Error: COHERE_API_KEY not found in .env file")
        return
    
    co = cohere.Client(cohere_api_key)
    
    # Get user input
    user_prompt = input("Enter your prompt: ")
    
    # Send request to Cohere
    try:
        response = co.generate(
            model="command",
            prompt=user_prompt,
            max_tokens=300,
            temperature=0.7,
        )
        
        # Display raw response
        print("\n" + "="*50)
        print("RAW COHERE RESPONSE:".center(50))
        print("="*50)
        print(response)
        
        # Display cleaned response
        print("\n" + "="*50)
        print("CLEANED RESPONSE:".center(50))
        print("="*50)
        print(response.generations[0].text)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("COHERE API TESTER")
    print("-----------------")
    main()
