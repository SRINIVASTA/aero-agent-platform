import streamlit as st

st.set_page_config(page_title="Aero AI Control Node", layout="wide")

# 1. Initialize persistent memory variables across page frames if empty
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "gemini_broken" not in st.session_state:
    st.session_state.gemini_broken = False

st.sidebar.title("🔐 App Access Control")

# --- CONSOLE CONDITION A: USER IS NOT LOGGED IN ---
if not st.session_state.authenticated:
    # Render Login Form Text Boxes
    app_password = st.sidebar.text_input("Enter App Password:", type="password", key="pwd_input")
    user_gemini_key = st.sidebar.text_input("Enter Your Gemini API Key:", type="password", key="key_input")

    if st.sidebar.button("🚀 Unlock Platform"):
        clean_pwd = app_password.strip()
        clean_key = user_gemini_key.strip()
        
        # Pull password from Streamlit Web Dashboard secrets with a failsafe default backup
        try:
            secret_password = st.secrets["auth"]["APP_PASSWORD"]
        except Exception:
            secret_password = "admin123"
        
        # Verify credentials structural formats
        if clean_pwd == secret_password and len(clean_key) > 0:
            st.session_state.authenticated = True
            st.session_state.api_key = clean_key
            st.session_state.gemini_broken = False  # Reset credit failure state flag on fresh login
            st.sidebar.success("🔑 Access Granted!")
            st.rerun() 
        else:
            st.session_state.authenticated = False
            if len(clean_key) == 0:
                st.sidebar.error("❌ Key Error: The Gemini API Key field cannot be left empty.")
            else:
                st.sidebar.error("❌ Password Error: Invalid password entered. Please try again.")

# --- CONSOLE CONDITION B: USER IS LOGGED IN (SHOW LOGOUT COMPONENT) ---
else:
    st.sidebar.success("✅ Session Active")
    st.sidebar.info(f"API Key Saved: `...{st.session_state.api_key[-6:] if len(st.session_state.api_key) > 6 else 'Active'}`")
    
    # 🔴 THE LOGOUT IMPLEMENTATION ACTION TRIGGER
    if st.sidebar.button("🔒 Logout & Lock System", type="primary"):
        # Explicitly scrub all structural keys out of Streamlit context memory partitions
        st.session_state.authenticated = False
        st.session_state.api_key = ""
        st.session_state.gemini_broken = False
        
        # Wipes customer temporary sandbox chat history arrays as well so data doesn't leak
        if "messages" in st.session_state:
            st.session_state.messages = []
        if "analytics_logs" in st.session_state:
            st.session_state.analytics_logs = []
            
        st.sidebar.warning("Session cleared. Locking framework.")
        st.rerun() # Instantly refreshes the view layout layout to re-render the login screens

# Main Page Layout Generation
st.title("💨 Aero Multi-Agent Orchestration Platform")

if st.session_state.authenticated:
    st.balloons() 
    st.markdown("""
    ### Core Operations Framework Launchpad
    This enterprise runtime dashboard links specialized language processing workflows into a unified customer interface.

    * **Go to 💬 Customer Chat** in the sidebar navigation links to launch user staging simulations.
    * **Go to 📊 Admin Metrics** in the sidebar navigation links to trace your model accuracy evaluation configurations.
    """)
else:
    st.error("🛑 Access Blocked. Please provide proper credentials in the left sidebar and click **Unlock Platform** to activate the processing nodes.")
