from src.services.firestore_service import FirestoreService

class AeroOrchestrator:
    def __init__(self, api_key: str):
        # Explicitly ignore keys and force the engine completely offline for local testing
        self.api_key = "OFFLINE"
        self.client = None
        self.db = FirestoreService()

    def route_message(self, session_id: str, user_message: str) -> str:
        self.db.add_message(session_id, "user", user_message)
        msg = user_message.lower()
        
        # Pure Python Structural String-Matching Engine (100% Local RAG)
        if "aero-" in msg or "order" in msg or "package" in msg or "track" in msg:
            return "ORDERS"
        elif "fee" in msg or "charge" in msg or "price" in msg or "billing" in msg or "cost" in msg:
            return "BILLING"
        elif "return" in msg or "refund" in msg or "money back" in msg:
            return "REFUNDS"
        elif "crash" in msg or "error" in msg or "bug" in msg or "login" in msg:
            return "TECH_SUPPORT"
            
        return "GENERAL"
