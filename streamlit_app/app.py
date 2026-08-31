import streamlit as st

st.set_page_config(page_title="Aero AI Control Node", layout="wide")

# Persistent state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

st.sidebar.title("🔐 App Access Control")

# Forms for credentials entry
app_password = st.sidebar.text_input("Enter App Password:", type="password", key="pwd_input")
user_gemini_key = st.sidebar.text_input("Enter Your Gemini API Key:", type="password", key="key_input")

if st.sidebar.button("🚀 Unlock Platform"):
    clean_pwd = app_password.strip()
    clean_key = user_gemini_key.strip()
    
    # Try to read from dashboard secrets. If it fails, default to admin123
    try:
        secret_password = st.secrets["auth"]["APP_PASSWORD"]
    except Exception:
        secret_password = "admin123"
    
    # REMOVED THE "AIza" REQUIREMENT RULE: Now it only checks that the password is right and the key field isn't empty!
    if clean_pwd == secret_password and len(clean_key) > 0:
        st.session_state.authenticated = True
        st.session_state.api_key = clean_key
        st.sidebar.success("🔑 Access Granted!")
        st.rerun() 
    else:
        st.session_state.authenticated = False
        if len(clean_key) == 0:
            st.sidebar.error("❌ Key Error: The Gemini API Key field cannot be left completely empty.")
        else:
            st.sidebar.error("❌ Password Error: Invalid password entered. Please try again.")

if st.session_state.authenticated:
    if st.sidebar.button("🔒 Lock System"):
        st.session_state.authenticated = False
        st.session_state.api_key = ""
        st.rerun()

st.title("💨 Aero Multi-Agent Orchestration Platform")

if st.session_state.authenticated:
    st.balloons() 
    st.markdown("""
    ### Core Operations Framework Launchpad
    This enterprise runtime dashboard links specialized language processing workflows into a unified customer interface.

    * **Go to 💬 Customer Chat** in the sidebar to launch user staging simulations.
    * **Go to 📊 Admin Metrics** in the sidebar to trace model accuracy configurations against test files.
    """)
else:
    st.error("🛑 Access Blocked. Please provide proper credentials in the left sidebar and click **Unlock Platform** to activate the processing nodes.")
