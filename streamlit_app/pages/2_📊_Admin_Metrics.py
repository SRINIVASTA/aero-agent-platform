import streamlit as st
import pandas as pd
import plotly.express as px
from src.tools.evaluator import PlatformEvaluator

st.title("📊 Platform Telemetry & Data Benchmark Suite")

# Multi-page persistent route security check guardrail
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("🛑 Access Blocked. Please return to the main App page and enter your credentials first.")
    st.stop()

st.subheader("🧪 Dataset Verification Diagnostic")
format_selection = st.radio("Select Evaluation Engine Input Source Layer:", ("CSV Data File", "JSON Data File"), horizontal=True)
chosen_format = "CSV" if "CSV" in format_selection else "JSON"

if st.button("🚀 Execute Pipeline System Audit"):
    evaluator = PlatformEvaluator(api_key=st.session_state.api_key)
    with st.spinner(f"Running validation rows parsed out of internal {chosen_format} structures..."):
        results_df = evaluator.run_evaluation(format_choice=chosen_format)
        total_runs = len(results_df)
        passes = len(results_df[results_df["Status"] == "✅ Pass"])
        accuracy_rate = (passes / total_runs) * 100
        
        st.success(f"Benchmark Run Finished! Accuracy: **{accuracy_rate:.1f}%** ({passes}/{total_runs} Rows Passed)")
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
