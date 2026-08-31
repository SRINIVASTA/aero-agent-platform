import sys
import os
import streamlit as st

# Force structural project paths sync
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Your local hardcoded RAG text files data
KB_BILLING_RAW = "📂 [LOCAL FILE SEARCH]: Subscription fees cost Rs.999/mo. Chargebacks trigger automatic account locks."
KB_ORDERS_RAW = "📂 [LOCAL FILE SEARCH]: Order AERO-100 Status: Package processed at Mumbai Hub. Out for delivery."
KB_REFUNDS_RAW = "📂 [LOCAL FILE SEARCH]: Refunds Policy: All processed inventory returns past the 30-day window must go through verification."
KB_TECH_RAW = "📂 [LOCAL FILE SEARCH]: Technical Manual: If experiencing application crashes, clear your app storage cache files."

st.title("💬 Aero Customer Staging Terminal")
st.info("⚠️ System Notice: Running in 100% Local File Search Mode (Gemini API Deactivated).")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize your offline orchestrator layout
from src.orchestrator import AeroOrchestrator
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = AeroOrchestrator(api_key="OFFLINE")

# Print chat history arrays
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Input your local query..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 1. Route intent completely locally using your custom string rules
    selected_route = st.session_state.orchestrator.route_message("session_demo", user_input)
    
    with st.chat_message("assistant"):
        with st.spinner(f"Searching local folders via [{selected_route}]..."):
            msg_lower = user_input.lower()
            
            # 2. Match intent directly to your raw data files
            if selected_route == "BILLING" or "fee" in msg_lower or "cost" in msg_lower:
                final_reply = KB_BILLING_RAW
            elif selected_route == "ORDERS" or "100" in msg_lower or "aero" in msg_lower:
                final_reply = KB_ORDERS_RAW
            elif selected_route == "TECH_SUPPORT" or "crash" in msg_lower:
                final_reply = KB_TECH_RAW
            elif selected_route == "REFUNDS" or "return" in msg_lower:
                final_reply = KB_REFUNDS_RAW
            else:
                final_reply = "📂 [LOCAL FILE SEARCH]: Query out of scope. Please search for keys like 'fee', 'order', or 'crash' to pull internal rules files."
            
            st.markdown(final_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": final_reply})
