import streamlit as st
import requests
import pandas as pd
import os 
# --- Configuration ---
st.set_page_config(page_title="Operator Control Panel", layout="wide", page_icon="🤖")

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# --- Reusable API Fetch Function ---
@st.cache_data(ttl=600) # Cache data for 10 minutes
def fetch_from_api(endpoint: str, params: dict = None):
    """
    Fetches data from a given API endpoint, handles errors, and returns the JSON data.
    """
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
    # Put search inputs in the sidebar for this page for a cleaner look
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

def ai_chat_page():
    st.header("AI Knowledge Base Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun() # Immediately rerun the script to clear the display

    if prompt := st.chat_input("Ask a question about the knowledge base..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    chat_url = f"{API_BASE_URL}/chat"
                    response = requests.post(chat_url, json={"query": prompt})
                    response.raise_for_status()
                    response_data = response.json()
                    
                    answer = response_data.get("answer", "Sorry, I couldn't get a valid answer.")
                    sources = response_data.get("sources", [])
                    
                    st.markdown(answer)
                    if sources:
                        with st.expander("View Sources"):
                            for source in sources:
                                st.info(source)
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})

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