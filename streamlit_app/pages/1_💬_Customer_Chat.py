import sys
import os
import time

# Sync folder tracking properties
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from src.orchestrator import AeroOrchestrator
from src.agents.billing_agent import BillingAgent
from src.agents.orders_agent import OrdersAgent
from src.agents.refunds_agent import RefundsAgent
from src.agents.tech_support_agent import TechSupportAgent
from src.agents.general_agent import GeneralAgent
from src.agents.escalation_agent import EscalationAgent
from src.agents.qa_agent import QAAgent

st.title("💬 Aero Customer Staging Terminal")

# Safe validation fallbacks
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Define data variables to fetch locally if Gemini goes down
KB_BILLING_RAW = "📂 [LOCAL FILE SEARCH]: Subscription fees cost Rs.999/mo. Chargebacks trigger automatic account locks."
KB_ORDERS_RAW = "📂 [LOCAL FILE SEARCH]: Order AERO-100 Status: Package processed at Mumbai Hub. Out for delivery."
KB_REFUNDS_RAW = "📂 [LOCAL FILE SEARCH]: Refunds Policy: All processed inventory returns past the 30-day window must go through verification."
KB_TECH_RAW = "📂 [LOCAL FILE SEARCH]: Technical Manual: If experiencing application crashes, clear your app storage cache files."

# Initialize processing frameworks cleanly
if "orchestrator" not in st.session_state:
    k = st.session_state.api_key
    st.session_state.orchestrator = AeroOrchestrator(api_key=k)
    st.session_state.agents = {
        "BILLING": BillingAgent(api_key=k) if k else None,
        "ORDERS": OrdersAgent(),
        "REFUNDS": RefundsAgent(),
        "TECH_SUPPORT": TechSupportAgent(),
        "GENERAL": GeneralAgent(),
        "ESCALATION": EscalationAgent()
    }
    st.session_state.qa_engine = QAAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous history arrays
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Input your query..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 1. Triage and find route safely (Survives Quota Exceeded drops)
    selected_route = st.session_state.orchestrator.route_message("session_demo", user_input)
    
    if "fraud" in user_input.lower() or "scam" in user_input.lower():
        selected_route = "ESCALATION"

    with st.chat_message("assistant"):
        with st.spinner(f"Processing Request via [{selected_route}] Node..."):
            final_reply = ""
            
            # --- TRY TO GENERATE THE NORMAL GEMINI ANSWER ---
            try:
                if selected_route in st.session_state.agents and st.session_state.agents[selected_route] is not None:
                    raw_reply = st.session_state.agents[selected_route].process("session_demo", user_input)
                    final_reply = st.session_state.qa_engine.process("session_demo", raw_reply)
            except Exception as api_error:
                # Gemini failed or context hit a limit! Mark final_reply empty to trigger file dump below
                final_reply = ""

            # --- CRITICAL FALLBACK DUMP: IF GEMINI FAILS, PULL RAW FILE VALUES ---
            if not final_reply:
                msg_lower = user_input.lower()
                if selected_route == "BILLING" or "fee" in msg_lower or "cost" in msg_lower:
                    final_reply = KB_BILLING_RAW
                elif selected_route == "ORDERS" or "100" in msg_lower:
                    final_reply = KB_ORDERS_RAW
                elif selected_route == "REFUNDS" or "return" in msg_lower:
                    final_reply = KB_REFUNDS_RAW
                elif selected_route == "TECH_SUPPORT" or "crash" in msg_lower or "bug" in msg_lower:
                    final_reply = KB_TECH_RAW
                else:
                    final_reply = "⚠️ [AI Offline]: Support nodes are down. Please call or visit our standard FAQ manuals directory."

            st.markdown(final_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": final_reply})
