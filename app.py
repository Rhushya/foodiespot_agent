import streamlit as st
import pandas as pd
from foodiespot_agent.agent import GroqAgent
from foodiespot_agent.restaurant_data import RESTAURANTS

# Initialize agent in session state if it doesn't exist
if 'agent' not in st.session_state:
    st.session_state.agent = GroqAgent()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for restaurant table visibility
if 'show_restaurants_table' not in st.session_state:
    st.session_state.show_restaurants_table = False

st.title("FoodieSpot Restaurant Reservation Agent")

# --- Display All Restaurants Section ---
st.subheader("All Available Restaurants")

# Button to toggle table visibility
if st.button("Show/Hide All Restaurants List"):
    st.session_state.show_restaurants_table = not st.session_state.show_restaurants_table

# Display the table if the state is True
if st.session_state.show_restaurants_table:
    if RESTAURANTS:
        # Convert restaurant data to a Pandas DataFrame for better display
        # Selecting specific fields to display for clarity, can be adjusted
        display_columns = ['id', 'name', 'cuisine', 'location', 'seating_capacity', 'hours', 'contact_info', 'average_rating']
        
        # Ensure all restaurants have these keys, providing defaults if not
        restaurants_df_data = []
        for r in RESTAURANTS:
            row = {col: r.get(col, 'N/A') for col in display_columns}
            restaurants_df_data.append(row)
            
        restaurants_df = pd.DataFrame(restaurants_df_data, columns=display_columns)
        st.dataframe(restaurants_df)
    else:
        st.write("No restaurant data available to display.")
# --- End of Display All Restaurants Section ---

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
