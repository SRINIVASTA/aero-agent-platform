import csv
import json
import os
import time
import pandas as pd
import streamlit as st
from src.orchestrator import AeroOrchestrator

class PlatformEvaluator:
    def __init__(self, api_key: str):
        # Allow fallback initialization if key missing/empty
        self.api_key = api_key if api_key else "OFFLINE"
        self.orchestrator = AeroOrchestrator(api_key=self.api_key)

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
            # Short delay block to maintain stable API connections
            time.sleep(0.2)
            msg = case["text"].lower()
            
            # 1. Check for manual override terms first
            if "fraud" in msg or "scam" in msg:
                actual_route = "ESCALATION"
            else:
                # --- PATHWAY A: Try Gemini Routing (If Credits Available) ---
                try:
                    # If a previous row already discovered Gemini is broken, skip the API call entirely
                    if st.session_state.get("gemini_broken", False):
                        raise ValueError("Gemini is flagged offline.")
                        
                    actual_route = self.orchestrator.route_message("eval_session", case["text"])
                
                # --- PATHWAY B: The Offline RAG Fallback Triage System ---
                except Exception:
                    # Flag the global system state so other components skip live calls immediately
                    st.session_state.gemini_broken = True
                    
                    # Exact local keyword matching rules to determine target node without Gemini
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
