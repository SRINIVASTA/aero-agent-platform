from src.agents.base_agent import BaseAgent
from google import genai
from google.genai import types

class BillingAgent(BaseAgent):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        with open("src/prompts/billing_prompt.txt", "r") as f:
            self.system_instruction = f.read()

    def process(self, session_id: str, user_message: str) -> str:
        kb_context = "Knowledge Base: Subscription fees cost Rs.999/mo. Chargebacks trigger automatic account locks."
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{kb_context}\n\nUser Question: {user_message}",
            config=types.GenerateContentConfig(system_instruction=self.system_instruction)
        )
        return response.text
