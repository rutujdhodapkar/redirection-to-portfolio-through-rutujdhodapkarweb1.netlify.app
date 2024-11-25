import streamlit as st
import pandas as pd
import time

# Path for the message CSV file
MSG_FILE = "msg.csv"

# Initialize the CSV file if it doesn't exist
def initialize_csv():
    try:
        df = pd.read_csv(MSG_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["username", "message"])
        df.to_csv(MSG_FILE, index=False)

# Function to fetch all messages from the CSV file
def get_messages():
    try:
        df = pd.read_csv(MSG_FILE)
        return df
    except Exception as e:
        st.error(f"Error reading messages: {e}")
        return pd.DataFrame(columns=["username", "message"])

# Function to save a new message in the CSV file
def save_message(username, message):
    try:
        df = pd.read_csv(MSG_FILE)
        df = df.append({"username": username, "message": message}, ignore_index=True)
        df.to_csv(MSG_FILE, index=False)
    except Exception as e:
        st.error(f"Error saving message: {e}")

# Streamlit app
def run_streamlit_app():
    st.title("Real-time Messaging System")

    # Initialize CSV if needed
    initialize_csv()

    # User login/username input
    username = st.text_input("Enter your username:")
    if not username:
        st.warning("Please enter a username!")
        return

    # Display chat messages
    st.write("**Chat Messages:**")
    df = get_messages()

    # Loop to display all messages and auto-refresh every second
    while True:
        # Display the chat history
        for idx, row in df.iterrows():
            st.write(f"{row['username']}: {row['message']}")

        # Refresh every second
        time.sleep(1)
        st.experimental_rerun()

    # Message input field and button to send a new message
    message = st.text_area("Enter your message:")
    if st.button("Send Message"):
        if message:
            save_message(username, message)
            st.success("Message sent!")
            st.experimental_rerun()
        else:
            st.warning("Please enter a message to send.")

if __name__ == "__main__":
    run_streamlit_app()
