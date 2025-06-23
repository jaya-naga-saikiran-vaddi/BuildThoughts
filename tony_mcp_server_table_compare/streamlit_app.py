import requests
import streamlit as st

st.title("Tony MCP Server UI - Table Comparator")

goal = st.text_input("Enter your goal", value="Compare actor table")
table = st.text_input("Enter table name", value="actor")

if st.button("Run MCP Flow"):
    payload = {"goal": goal, "table_name": table}
    with st.spinner("Running..."):
        response = requests.post("http://localhost:8000/run-job", json=payload)
        result = response.json()
        st.success("Goal Processed!")
        st.json(result)
