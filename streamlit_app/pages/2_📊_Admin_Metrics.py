import sys
import os

# Sync workspace directory boundaries
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.tools.evaluator import PlatformEvaluator

st.title("📊 Platform Telemetry & Data Benchmark Suite")

# Global fallback state initialization
if "gemini_broken" not in st.session_state:
    st.session_state.gemini_broken = False

# Live status system banners
if st.session_state.gemini_broken:
    st.error("⚠️ System Notice: Gemini Credits Exhausted (429). Benchmark suite is running on 100% Offline Local Matching rules.")
else:
    st.success("🌐 System Status: Active Cloud Engine Running.")

st.subheader("🧪 Dataset Verification Diagnostic")
format_selection = st.radio("Select Evaluation Engine Input Source Layer:", ("CSV Data File", "JSON Data File"), horizontal=True)
chosen_format = "CSV" if "CSV" in format_selection else "JSON"

if st.button("🚀 Execute Pipeline System Audit"):
    # Grab the key securely from memory state
    user_key = st.session_state.get("api_key", "")
    evaluator = PlatformEvaluator(api_key=user_key)
    
    with st.spinner(f"Running validation rows parsed out of internal {chosen_format} structures..."):
        # Executes the safe evaluation loop that catches exceptions
        results_df = evaluator.run_evaluation(format_choice=chosen_format)
        total_runs = len(results_df)
        passes = len(results_df[results_df["Status"] == "✅ Pass"])
        accuracy_rate = (passes / total_runs) * 100
        
        st.success(f"Benchmark Run Finished! Calculated Accuracy: **{accuracy_rate:.1f}%** ({passes}/{total_runs} Rows Passed)")
        st.dataframe(results_df, use_container_width=True)

st.markdown("---")
st.subheader("📈 Live Session Operational Metrics")

if "analytics_logs" not in st.session_state or len(st.session_state.analytics_logs) == 0:
    st.info("No runtime application interactions tracked yet. Populate chat history to drive charts.")
    df_metrics = pd.DataFrame([
        {"timestamp": "00:00:00", "route": "GENERAL", "latency": 0.4, "escalation_triggered": 0}
    ])
else:
    df_metrics = pd.DataFrame(st.session_state.analytics_logs)

col_left, col_right = st.columns(2)
with col_left:
    fig_pie = px.pie(df_metrics, names="route", hole=0.4, title="Node Load Balancing Breakdown", color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig_pie, use_container_width=True)
with col_right:
    fig_line = px.line(df_metrics, x="timestamp", y="latency", markers=True, title="Model Processing Speeds Over Time")
    st.plotly_chart(fig_line, use_container_width=True)
