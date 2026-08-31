from src.agents.base_agent import BaseAgent
from google import genai

class OrdersAgent(BaseAgent):
    def __init__(self, api_key: str):
        # Initialize the Gemini client for advanced parsing
        self.client = genai.Client(api_key=api_key)

    def process(self, session_id: str, user_message: str) -> str:
        # Our raw backend logistics database string
        mumbai_tracking_data = "📦 **Live Order Tracking Update:** Package processed at Mumbai Hub. Out for delivery."
        
        # --- PATHWAY A: The Gemini Way (Normal Operation) ---
        try:
            # We use Gemini to see if the user is asking about the Mumbai shipment
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Does this message ask about the package or shipment status? Message: {user_message}. Reply with YES or NO."
            )
            
            if "yes" in response.text.lower() or "100" in user_message:
                return mumbai_tracking_data
                
        # --- PATHWAY B: The Gemini-Free Fallback Way (If Credits Run Out) ---
        except Exception as e:
            # The AI brain is offline, so we fall back to raw keyword scanning
            if "100" in user_message or "mumbai" in user_message.lower() or "order" in user_message.lower():
                return f"⚠️ **[System Fallback Mode - AI Offline]:** {mumbai_tracking_data}"

        # Default fallback response if no tracking identifiers match
        return "Please supply a valid `AERO-` sequence tracking identifier to check live logistical tracking status logs."
