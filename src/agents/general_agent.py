from src.agents.base_agent import BaseAgent

class GeneralAgent(BaseAgent):
    def process(self, session_id: str, user_message: str) -> str:
        return "👋 **Aero General Assistant:** Hello! Welcome to Aero Support. I am here to assist with general information. Our normal business hours are 9 AM to 6 PM."
