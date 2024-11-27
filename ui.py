import streamlit as st
import requests
# from rag import rag_chain

def ask_questions(query):
    """
    Makes a POST request to the RAG API endpoint with the given query.

    Args:
        query (str): The query string to send in the request body.

    Returns:
        dict: A dictionary containing the API response or an error message.
    """
    headers = {
        "Content-Type": "application/json",
    }

    # Include the function key in the query string if provided
    # if function_key:
    endpoint_url = st.secrets['ENDPOINT_URL']

    payload = {"query": query}

    try:
        response = requests.post(endpoint_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Parse the JSON response body
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {str(e)}"}

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("RAG Simple Chat Interface")

# Input box for the user's query
user_input = st.text_input(
    "Ask your question:",
    placeholder="Type your question and press Enter...",
    key="user_input",
)

# Process user input
if user_input:
    # Append user query to session state
    st.session_state.messages.append(f"You: {user_input}")

    # Process the input with your RAG chain
    # Replace `rag_chain` with your actual RAG chain
    try:
        with st.spinner("Generating response..."):
            response = ask_questions(user_input)  # Adjust if needed
            assistant_response = response.get("result", "Sorry, I couldn't find an answer.")
    except Exception as e:
        assistant_response = f"An error occurred: {str(e)}"


    # Display the conversation history
    st.markdown("### Results")
    st.markdown(assistant_response)
    for i, s in enumerate(response.get('source_documents')):
        with st.status(f'Reference {i}'):
            st.write(s['context'])
            st.write(s['title'])
            st.write(s['content'])
