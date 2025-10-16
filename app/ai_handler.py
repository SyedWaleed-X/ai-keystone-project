import google.generativeai as genai

import os 

import traceback

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)


def get_llm_completion(prompt: str):


    try:

        model = genai.GenerativeModel("gemini-2.5-pro")

        response_stream = model.generate_content(prompt,stream=True)

        for chunk in response_stream:
            # Yield each piece of text as it comes in
            yield chunk.text
    
    except Exception as e:
        print(f"--- AN ERROR OCCURRED IN AI_HANDLER ---")
        traceback.print_exc()
        yield "Error: Could not get a response from the AI model."
