import sys
import os
import time

# Sync folder tracking properties
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st

# Global system state flags initialization
if "gemini_broken" not in st.session_state:
    st.session_state.gemini_broken = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Define local data variables to fetch locally if Gemini goes down
KB_BILLING_RAW = "📂 [OFFLINE RAG LOCAL CHIP]: Subscription fees cost Rs.999/mo. Chargebacks trigger automatic account locks."
KB_ORDERS_RAW = "📦 [OFFLINE RAG LOCAL CHIP]: Order AERO-100 Status: Package processed at Mumbai Hub. Out for delivery."
KB_REFUNDS_RAW = "📂 [OFFLINE RAG LOCAL CHIP]: Refunds Policy: All processed inventory returns past the 30-day window must go through verification."
KB_TECH_RAW = "📂 [OFFLINE RAG LOCAL CHIP]: Technical Manual: If experiencing application crashes, clear your app storage cache files."

st.title("💬 Aero Customer Staging Terminal")

# Visual indicator showing system running mode layout status
if st.session_state.gemini_broken:
    st.error("⚠️ System Status: Gemini Credits Exhausted (429). Operating in 100% Offline RAG Backup Mode.")
else:
    st.success("🌐 System Status: Active Cloud Engine Running.")

# Import orchestrator engine framework properties
from src.orchestrator import AeroOrchestrator
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = AeroOrchestrator(api_key=st.session_state.get("api_key", ""))

# Render historical communication feeds
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Input your query..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 1. Safe Routing Processing Check
    selected_route = "GENERAL"
    try:
        selected_route = st.session_state.orchestrator.route_message("session_demo", user_input)
    except Exception:
        st.session_state.gemini_broken = True
        msg_lower = user_input.lower()
        if "aero-" in msg_lower or "order" in msg_lower:
            selected_route = "ORDERS"
        elif "fee" in msg_lower or "cost" in msg_lower:
            selected_route = "BILLING"

    # 2. Response Parsing Action Block
    with st.chat_message("assistant"):
        with st.spinner(f"Processing requests via [{selected_route}]..."):
            final_reply = ""
            
            # Try running active cloud parameters if model is not flagged broken
            if not st.session_state.gemini_broken:
                try:
                    from src.agents.billing_agent import BillingAgent
                    if selected_route == "BILLING":
                        agent = BillingAgent(api_key=st.session_state.api_key)
                        final_reply = agent.process("session_demo", user_input)
                except Exception:
                    st.session_state.gemini_broken = True

            # --- THE OFFLINE RAG BACKUP TAKE-OVER ---
            # If Gemini failed or is broken, look up the raw local strings instantly
            if not final_reply:
                msg_lower = user_input.lower()
                if selected_route == "BILLING" or "fee" in msg_lower or "cost" in msg_lower:
                    final_reply = KB_BILLING_RAW
                elif selected_route == "ORDERS" or "100" in msg_lower or "aero" in msg_lower:
                    final_reply = KB_ORDERS_RAW
                elif selected_route == "TECH_SUPPORT" or "crash" in msg_lower:
                    final_reply = KB_TECH_RAW
                elif selected_route == "REFUNDS" or "return" in msg_lower:
                    final_reply = KB_REFUNDS_RAW
                else:
                    final_reply = "📂 [OFFLINE RAG LOCAL CHIP]: Search term out of scope. Use terms like 'fee', 'order', or 'crash' to pull local files."

            st.markdown(final_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": final_reply})
