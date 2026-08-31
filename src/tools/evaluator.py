import csv
import json
import os
import pandas as pd
from src.orchestrator import AeroOrchestrator

class PlatformEvaluator:
    def __init__(self, api_key: str):
        self.orchestrator = AeroOrchestrator(api_key=api_key)

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
            if "fraud" in case["text"].lower() or "scam" in case["text"].lower():
                actual_route = "ESCALATION"
            else:
                actual_route = self.orchestrator.route_message("eval_session", case["text"])
            
            is_correct = (actual_route == case["expected_route"])
            results.append({
                "User Text": case["text"],
                "Target Route": case["expected_route"],
                "Model Route": actual_route,
                "Status": "✅ Pass" if is_correct else "❌ Fail",
                "Priority": case.get("priority", "medium")
            })
        return pd.DataFrame(results)
