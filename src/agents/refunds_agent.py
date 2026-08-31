from src.agents.base_agent import BaseAgent

class RefundsAgent(BaseAgent):
    def process(self, session_id: str, user_message: str) -> str:
        return "🔄 **Refund Policy Manager:** All processed inventory returns submitted past the standard 30-day corporate window must go through standard verification pipelines."
