# In app_frontend.py

import streamlit as st
import requests
import pandas as pd
import os
import time # <-- Make sure to import the time library

# --- Configuration ---
st.set_page_config(page_title="Operator Control Panel", layout="wide", page_icon="🤖")

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# --- Reusable API Fetch Function ---
@st.cache_data(ttl=600)
def fetch_from_api(endpoint: str, params: dict = None):
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error at '{endpoint}': {e}")
        return None

# --- Page Definitions ---

def home_page():
    st.header("Welcome to the Operator's Control Panel")
    st.write("Use the navigation bar on the left to access different modules.")
    st.info("This application provides a user-friendly interface for the AI Keystone Project API, allowing interaction with both the structured employee database and the unstructured AI knowledge base.")

def employee_data_page():
    st.header("Employee Data Management")
    st.subheader("Full Data Views")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Fetch All Employees"):
            data = fetch_from_api("employees")
            if data:
                st.dataframe(pd.DataFrame(data))
    with col2:
        if st.button("Fetch All Departments"):
            data = fetch_from_api("departments")
            if data:
                st.dataframe(pd.DataFrame(data))
    st.divider()
    st.subheader("Search and Filter Employees")
    st.sidebar.header("Employee Filters")
    emp_id = st.sidebar.number_input("Fetch by Employee ID:", min_value=1, step=1, value=None)
    if st.sidebar.button("Fetch by ID"):
        if emp_id:
            data = fetch_from_api(f"employees/{emp_id}")
            if data:
                st.write("Employee Found:")
                st.dataframe(pd.DataFrame([data]))
    dep_name = st.sidebar.text_input("Filter by Department:")
    min_salary = st.sidebar.number_input("Filter by Minimum Salary:", min_value=0, step=1000, value=None)
    if st.sidebar.button("Filter Employees"):
        search_params = {}
        if dep_name: search_params["department"] = dep_name
        if min_salary: search_params["min_salary"] = min_salary
        data = fetch_from_api("search/employees", params=search_params)
        if data is not None:
            if not data:
                st.warning("No employees found matching the criteria.")
            else:
                st.write(f"Found {len(data)} matching employees:")
                st.dataframe(pd.DataFrame(data))

# --- THIS IS THE FINAL, CORRECTED CHAT PAGE FUNCTION ---
def ai_chat_page():
    st.header("AI Knowledge Base Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages and their sources
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "source_documents" in message and message["source_documents"]:
                with st.expander("View Sources"):
                    for i, doc in enumerate(message["source_documents"]):
                        metadata = message["source_metadatas"][i]
                        filename = metadata.get("source", "N/A")
                        page = metadata.get("page")
                        
                        # Create the header for the blue box
                        if page is not None:
                            source_header = f"Source: {filename}, Page: {page + 1}"
                        else:
                            source_header = f"Source: {filename}"
                        
                        st.info(source_header)
                        st.text(doc) # Display the actual text chunk

    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    if prompt := st.chat_input("Ask a question about the knowledge base..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # --- NEW WAITING UX ---
            with st.spinner("Finding relevant documents..."):
                time.sleep(3) # Simulate a 3-second search

            with st.spinner("Thinking..."):
                try:
                    chat_url = f"{API_BASE_URL}/chat"
                    response = requests.post(chat_url, json={"query": prompt})
                    response.raise_for_status()
                    response_data = response.json()
                    
                    answer = response_data.get("answer")
                    source_documents = response_data.get("source_documents", [])
                    source_metadatas = response_data.get("source_metadatas", [])
                    
                    # Display the final answer
                    st.markdown(answer)
                    
                    # Save the complete message to session state for the next rerun
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "source_documents": source_documents,
                        "source_metadatas": source_metadatas
                    })
                    # Rerun the script to display the new "View Sources" expander
                    st.rerun()

                except requests.exceptions.RequestException as e:
                    error_message = f"API Error: {e}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})

# --- Main App Navigation ---
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio(
    "Choose a module:",
    ["Home", "Employee Data", "AI Knowledge Chat"]
)
st.sidebar.divider()
st.sidebar.info("This is the frontend for the AI Keystone Project.")
st.sidebar.info("Built by Syed Waleed-X.")

if app_mode == "Home":
    home_page()
elif app_mode == "Employee Data":
    employee_data_page()
elif app_mode == "AI Knowledge Chat":
    ai_chat_page()