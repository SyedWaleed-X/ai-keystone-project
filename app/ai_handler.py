import google.generativeai as genai

import  config 

import traceback


genai.configure(api_key=config.GEMINI_API_KEY)


def get_llm_completion(prompt: str) -> str:


    try:

        model = genai.GenerativeModel("gemini-2.5-pro")

        response = model.generate_content(prompt)

        return response.text.strip()
    
    except Exception as e:
        print("an error occured")

        return "error, couldnt get a response from AI "
