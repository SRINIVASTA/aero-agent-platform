class QAAgent:
    def process(self, session_id: str, raw_agent_response: str) -> str:
        if "password" in raw_agent_response.lower() or "secret" in raw_agent_response.lower():
            return "System Warning: A data compliance error was avoided. Blocked response content leakage."
        return raw_agent_response
