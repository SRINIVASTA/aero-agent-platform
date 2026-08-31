import streamlit as st
import time
from src.orchestrator import AeroOrchestrator
from src.agents.billing_agent import BillingAgent
from src.agents.orders_agent import OrdersAgent
from src.agents.refunds_agent import RefundsAgent
from src.agents.tech_support_agent import TechSupportAgent
from src.agents.general_agent import GeneralAgent
from src.agents.escalation_agent import EscalationAgent
from src.agents.qa_agent import QAAgent

st.title("💬 Aero Customer Staging Terminal")

# Multi-page persistent route security check guardrail
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("🛑 Access Blocked. Please return to the main App page and enter your credentials first.")
    st.stop()

if "orchestrator" not in st.session_state:
    k = st.session_state.api_key
    st.session_state.orchestrator = AeroOrchestrator(api_key=k)
    st.session_state.agents = {
        "BILLING": BillingAgent(api_key=k),
        "ORDERS": OrdersAgent(),
        "REFUNDS": RefundsAgent(),
        "TECH_SUPPORT": TechSupportAgent(),
        "GENERAL": GeneralAgent(),
        "ESCALATION": EscalationAgent()
    }
    st.session_state.qa_engine = QAAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "analytics_logs" not in st.session_state:
    st.session_state.analytics_logs = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Input your query..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    start_time = time.time()
    selected_route = st.session_state.orchestrator.route_message("session_demo", user_input)
    
    if "fraud" in user_input.lower() or "scam" in user_input.lower():
        selected_route = "ESCALATION"

    with st.chat_message("assistant"):
        with st.spinner(f"Routing to [{selected_route}] core..."):
            if selected_route in st.session_state.agents:
                raw_reply = st.session_state.agents[selected_route].process("session_demo", user_input)
            else:
                raw_reply = st.session_state.agents["GENERAL"].process("session_demo", user_input)
            
            final_reply = st.session_state.qa_engine.process("session_demo", raw_reply)
            st.markdown(final_reply)

    end_time = time.time()
    execution_latency = round(end_time - start_time, 2)
    
    st.session_state.analytics_logs.append({
        "timestamp": time.strftime("%H:%M:%S"),
        "route": selected_route,
        "latency": execution_latency,
        "escalation_triggered": 1 if selected_route == "ESCALATION" or "human" in final_reply.lower() else 0
    })
    st.session_state.messages.append({"role": "assistant", "content": final_reply})
