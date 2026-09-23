import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="DataOps Observability",
    layout="wide"
)

st.title("DataOps Observability Dashboard")

RUN_LOG = "data/monitoring/run_history.csv"
SLA_LOG = "data/monitoring/sla_history.csv"

if not os.path.exists(RUN_LOG):
    st.error("No pipeline run history found.")
    st.stop()

runs = pd.read_csv(RUN_LOG)

st.subheader("Pipeline Run Summary")

latest = runs.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Run Status", latest["status"])
col2.metric("Input Rows", latest["input_rows"])
col3.metric("Output Rows", latest["output_rows"])
col4.metric("Duration (sec)", latest["duration_seconds"])

st.subheader("Data Quality & SLA")

col1, col2, col3 = st.columns(3)

col1.metric("Data Quality", latest["quality_status"])
col2.metric("Freshness", latest["freshness_status"])
col3.metric("SLA", latest["sla_status"])

st.subheader("Run History")

st.dataframe(
    runs,
    use_container_width=True
)

if os.path.exists(SLA_LOG):
    st.subheader("SLA History")
    sla = pd.read_csv(SLA_LOG)
    st.dataframe(
        sla,
        use_container_width=True
    )

if latest["status"] == "FAILED":
    st.error(
        f"Incident detected. "
        f"Failed stage: {latest['failed_stage']} | "
        f"Error: {latest['error_message']}"
    )
else:
    st.success("Latest pipeline run completed successfully.")
