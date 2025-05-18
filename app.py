import streamlit as st
from foodiespot_agent.agent import GroqAgent # Import the agent

# Basic Streamlit app structure
st.title("FoodieSpot Restaurant Reservation Agent")

# Initialize agent in session state if it doesn't exist
if 'agent' not in st.session_state:
    st.session_state.agent = GroqAgent()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("Ask me about restaurant reservations:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Use the agent from session state
            response = st.session_state.agent.handle_user_query(user_input)
            st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
