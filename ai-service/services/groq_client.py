import os
import json
from groq import Groq

class GroqClient:
    def __init__(self):
        # AI Developer 2 builds this, but we need it for Day 3 & 4 testing
        self.api_key = os.getenv("GROQ_API_KEY", "")
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None
        self.model = "llama-3.3-70b-versatile"

    def generate_response(self, prompt, is_json=False):
        if not self.client:
            return json.dumps({"error": "No Groq API key set."}) if is_json else "Error: No API key."
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.3, # 0.3 for factual as per Day 9 hint
                response_format={"type": "json_object"} if is_json else None
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Groq API Error: {e}")
            if is_json:
                return json.dumps({"is_fallback": True, "error": str(e)})
            return "Fallback error response."
