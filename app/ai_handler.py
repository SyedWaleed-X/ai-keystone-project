# ai_handler.py
import google.generativeai as genai
import config # Our safe file for the API key

# 1. Configure the client with your API key
genai.configure(api_key=config.GEMINI_API_KEY)

# 2. Create the model instance
model = genai.GenerativeModel('gemini-2.5-pro')

def get_llm_completion(prompt: str) -> str:
    """
    Sends a prompt to the Gemini API and returns the text response.
    """
    try:
        # 3. Send the prompt to the model
        response = model.generate_content(prompt)
        
        # 4. Return the text part of the response
        return response.text
    except Exception as e:
        # Basic error handling
        print(f"An error occurred: {e}")
        return "Error: Could not get a response from the model."