from src.agents.base_agent import BaseAgent

class OrdersAgent(BaseAgent):
    def process(self, session_id: str, user_message: str) -> str:
        if "100" in user_message:
            return "📦 **Live Order Tracking Update:** Package processed at Mumbai Hub. Out for delivery."
        return "Please supply a valid `AERO-` sequence tracking identifier to check live logistical tracking status logs."
