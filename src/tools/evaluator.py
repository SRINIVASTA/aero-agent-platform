import csv
import json
import os
import time
import pandas as pd
import streamlit as st
from src.orchestrator import AeroOrchestrator

class PlatformEvaluator:
    def __init__(self, api_key: str):
        self.api_key = api_key if api_key else "OFFLINE"
        # Only initialize the live orchestrator object if Gemini isn't already flagged as broken
        if not st.session_state.get("gemini_broken", False) and self.api_key != "OFFLINE":
            self.orchestrator = AeroOrchestrator(api_key=self.api_key)
        else:
            self.orchestrator = None

    def load_from_csv(self, file_path="data/evaluation_dataset.csv") -> list:
        dataset = []
        if os.path.exists(file_path):
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    dataset.append(row)
        return dataset

    def load_from_json(self, file_path="data/evaluation_dataset.json") -> list:
        if os.path.exists(file_path):
            with open(file_path, mode='r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def run_evaluation(self, format_choice="CSV") -> pd.DataFrame:
        test_cases = self.load_from_csv() if format_choice.upper() == "CSV" else self.load_from_json()
        results = []
        
        for case in test_cases:
            msg = case["text"].lower()
            
            # Rule 1: Instant static check for critical escalation terms
            if "fraud" in msg or "scam" in msg:
                actual_route = "ESCALATION"
            else:
                # --- PATHWAY A: Try Live Gemini Routing (Only if completely clear and working) ---
                if self.orchestrator and not st.session_state.get("gemini_broken", False):
                    try:
                        time.sleep(0.2) # Prevent rapid API connection bursts
                        actual_route = self.orchestrator.route_message("eval_session", case["text"])
                    except Exception:
                        # If a quota boundary error hits mid-run, instantly toggle offline mode
                        st.session_state.gemini_broken = True
                        self.orchestrator = None
                        actual_route = "LOCAL_FALLBACK"
                else:
                    actual_route = "LOCAL_FALLBACK"

                # --- PATHWAY B: Pure Python String-Matching (Offline Local RAG Engine) ---
                # This catches the fallback row execution if Gemini is disabled/exhausted
                if actual_route == "LOCAL_FALLBACK":
                    if "aero-" in msg or "order" in msg or "package" in msg or "track" in msg:
                        actual_route = "ORDERS"
                    elif "fee" in msg or "charge" in msg or "price" in msg or "billing" in msg or "cost" in msg:
                        actual_route = "BILLING"
                    elif "return" in msg or "refund" in msg or "money back" in msg:
                        actual_route = "REFUNDS"
                    elif "crash" in msg or "error" in msg or "bug" in msg or "login" in msg:
                        actual_route = "TECH_SUPPORT"
                    else:
                        actual_route = "GENERAL"
            
            is_correct = (actual_route == case["expected_route"])
            results.append({
                "User Text": case["text"],
                "Target Route": case["expected_route"],
                "Model Route": f"{actual_route} (Offline RAG)" if st.session_state.get("gemini_broken", False) and actual_route != "ESCALATION" else actual_route,
                "Status": "✅ Pass" if is_correct else "❌ Fail",
                "Priority": case.get("priority", "medium")
            })
            
        return pd.DataFrame(results)
