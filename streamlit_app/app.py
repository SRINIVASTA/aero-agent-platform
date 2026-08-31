import streamlit as st

st.set_page_config(page_title="Aero AI Control Node", layout="wide")

# App Locking Layer Integration
st.sidebar.title("🔐 App Access Control")
app_password = st.sidebar.text_input("Enter App Password:", type="password")
user_gemini_key = st.sidebar.text_input("Enter Your Gemini API Key:", type="password")

# Set global verification states
# CHANGE "admin123" to any password you want for your application!
if app_password == "admin123" and user_gemini_key.startswith("AIza"):
    st.session_state.authenticated = True
    st.session_state.api_key = user_gemini_key
    st.sidebar.success("🔑 System Unlocked Successfully!")
else:
    st.session_state.authenticated = False
    st.sidebar.warning("Please enter the correct App Password and a valid Gemini API Key to continue.")

st.title("💨 Aero Multi-Agent Orchestration Platform")

if st.session_state.authenticated:
    st.markdown("""
    ### Core Operations Framework Launchpad
    This enterprise runtime dashboard links specialized language processing workflows into a unified customer interface.

    * **Go to 💬 Customer Chat** to launch user staging simulations.
    * **Go to 📊 Admin Metrics** to trace model classification accuracy configurations against verification data files.
    """)
else:
    st.error("🛑 Access Blocked. Please provide proper credentials in the left sidebar to activate the processing nodes.")
