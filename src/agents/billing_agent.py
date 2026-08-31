import os
from src.agents.base_agent import BaseAgent
from google import genai
from google.genai import types

class BillingAgent(BaseAgent):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        with open("src/prompts/billing_prompt.txt", "r") as f:
            self.system_instruction = f.read()

    def process(self, session_id: str, user_message: str) -> str:
        # This is your raw internal Knowledge Base file data
        kb_text = "Knowledge Base Fact: Standard premium subscription platform fees cost Rs.999/mo. Chargebacks trigger automatic account locks."
        
        # --- PATHWAY A: The Gemini Way (Normal Operation) ---
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"{kb_text}\n\nUser Question: {user_message}",
                config=types.GenerateContentConfig(system_instruction=self.system_instruction)
            )
            return response.text
            
        # --- PATHWAY B: The Gemini-Free Fallback Way (If Credits Run Out) ---
        except Exception as e:
            # The AI brain is dead/out of credits, so the app handles it manually
            # 1. Look for keywords in what the user typed
            if "fee" in user_message.lower() or "charge" in user_message.lower() or "price" in user_message.lower() or "cost" in user_message.lower():
                # 2. Return the raw text string directly from your file without changing it
                return f"⚠️ **[System Fallback Mode - AI Offline]:** {kb_text}"
            
            # 3. Default fallback statement if no keywords match your database strings
            return "⚠️ **[System Fallback Mode - AI Offline]:** Our support AI is currently undergoing maintenance. Please visit our help docs or contact a human representative."
