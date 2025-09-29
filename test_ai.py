# test_ai.py
from app.ai_handler import get_llm_completion

test_prompt = "What are the three main benefits of using Python for web development?"

print(f"Sending prompt: '{test_prompt}'")
response = get_llm_completion(test_prompt)
print("\n--- LLM Response ---")
print(response)
print("--------------------")