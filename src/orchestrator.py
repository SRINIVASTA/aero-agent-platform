import json
import streamlit as st
from google import genai
from google.genai import types
from src.services.firestore_service import FirestoreService

class AeroOrchestrator:
    def __init__(self, api_key: str):
        self.api_key = api_key if api_key else "OFFLINE"
        self.db = FirestoreService()
        
        # Load rule parameters safely
        try:
            with open("src/prompts/router_prompt.txt", "r") as f:
                self.system_instruction = f.read()
        except Exception:
            self.system_instruction = "Fallback Routing Rules"

        # Initialize the API client
        try:
            if self.api_key != "OFFLINE" and not st.session_state.get("gemini_broken", False):
                self.client = genai.Client(api_key=api_key)
            else:
                self.client = None
        except Exception:
            self.client = None

    def route_message(self, session_id: str, user_message: str) -> str:
        self.db.add_message(session_id, "user", user_message)
        msg = user_message.lower()
        
        # --- PATHWAY A: The Gemini Router (Normal Operation with Credits) ---
        # FIXED: Added strict try/except blocks inside the actual routing engine line execution
        if self.client and not st.session_state.get("gemini_broken", False):
            try:
                full_history = self.db.get_history(session_id)
                recent_history = full_history[-5:] if len(full_history) > 5 else full_history
                context = "\n".join([f"{m['role']}: {m['content']}" for m in recent_history])
                
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Determine route for the following history:\n{context}",
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        response_mime_type="application/json"
                    )
                )
                cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
                route_data = json.loads(cleaned_text)
                return route_data.get("route", "GENERAL")
            except Exception:
                # INTERCEPT CODES: Catch 429 errors safely, save the failure flag, and drop straight to local data
                st.session_state.gemini_broken = True

        # --- PATHWAY B: Pure Python String-Matching (Your Offline RAG Fallback) ---
        if "aero-" in msg or "order" in msg or "package" in msg or "track" in msg:
            return "ORDERS"
        elif "fee" in msg or "charge" in msg or "price" in msg or "billing" in msg or "cost" in msg:
            return "BILLING"
        elif "return" in msg or "refund" in msg or "money back" in msg:
            return "REFUNDS"
        elif "crash" in msg or "error" in msg or "bug" in msg or "login" in msg:
            return "TECH_SUPPORT"
            
        return "GENERAL"
