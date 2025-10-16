import streamlit as st
import requests
import pandas as pd
import os
import json

# --- Configuration ---
st.set_page_config(page_title="Operator Control Panel", layout="wide", page_icon="🤖")

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# --- Reusable API Fetch Function (for non-streaming endpoints) ---
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
    # ... (This function is correct, no changes needed) ...
    st.header("Welcome to the Operator's Control Panel")
    st.write("Use the navigation bar on the left to access different modules.")
    st.info("This application provides a user-friendly interface for the AI Keystone Project API, allowing interaction with both the structured employee database and the unstructured AI knowledge base.")

def employee_data_page():
    # ... (This function is correct, no changes needed) ...
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

# --- THIS IS THE NEW, CORRECTED CHAT PAGE FUNCTION ---
def ai_chat_page():
    st.header("AI Knowledge Base Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # Check if there are sources and display them beautifully
            if "sources" in message and message["sources"]:
                with st.expander("View Sources"):
                    for source_doc, source_meta in zip(message["source_documents"], message["sources"]):
                        st.info(f"**Source:** {source_meta.get('source', 'N/A')}, **Page:** {source_meta.get('page', 'N/A') + 1 if source_meta.get('page') is not None else 'N/A'}")
                        st.text(source_doc)


    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    # Handle new user input
    if prompt := st.chat_input("Ask a question about the knowledge base..."):
        # Add user message to history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response by streaming
        with st.chat_message("assistant"):
            full_response_text = ""
            sources = []
            source_documents = [] # We need to get the source documents as well

            # Use st.write_stream which is designed for this exact purpose
            def stream_generator():
                url = f"{API_BASE_URL}/chat"
                with requests.post(url, json={"query": prompt}, stream=True) as r:
                    r.raise_for_status()
                    for line in r.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            if decoded_line.startswith("SOURCES:::"):
                                # This is our special end-of-stream message
                                sources_data = json.loads(decoded_line.split("SOURCES:::", 1)[1])
                                # We need to update the RAG pipeline to send both docs and metadata
                                nonlocal sources
                                nonlocal source_documents
                                sources = sources_data.get("metadatas", [])
                                source_documents = sources_data.get("documents", [])
                            else:
                                # This is a regular text chunk
                                yield decoded_line
            
            # st.write_stream will display the text chunks as they arrive
            streamed_text = st.write_stream(stream_generator)

        # After the stream is complete, save the full message to state
        st.session_state.messages.append({
            "role": "assistant",
            "content": streamed_text,
            "sources": sources,
            "source_documents": source_documents,
        })
        # Rerun to make the "View Sources" expander appear on the new message
        st.rerun()


# --- Main App Navigation ---
# ... (The rest of your file is correct, no changes needed) ...
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