from app.ai_handler import get_llm_completion


prompt  = "yoo whats up bro this is an api call yoo ehehehe"

print(f"Sending prompt {prompt}")


ai_response = get_llm_completion(prompt)

print(f"the ai responded with : {ai_response}")

