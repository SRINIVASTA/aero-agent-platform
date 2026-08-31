from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def process(self, session_id: str, user_message: str) -> str:
        pass
