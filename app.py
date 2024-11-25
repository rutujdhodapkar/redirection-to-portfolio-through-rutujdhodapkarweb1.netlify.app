import streamlit as st
import pandas as pd
import time

# Function to read and update CSV file with new messages
def update_messages(message, username):
    # Read existing messages
    try:
        df = pd.read_csv('msg.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["username", "message"])
    
    # Add new message
    new_message = {"username": username, "message": message}
    df = df.append(new_message, ignore_index=True)
    
    # Keep only the last 10 messages
    df = df.tail(10)
    
    # Save the updated dataframe to CSV
    df.to_csv('msg.csv', index=False)

# Streamlit UI components
st.title("Message Board")

# User inputs
username = st.text_input("Enter your username:", "")
if username:
    # Only show message input box when username is entered
    message = st.text_input("Enter your message:", "")
    send_button = st.button("Send")

    if send_button and message:
        update_messages(message, username)
        st.success("Message sent!")

# Display last 10 messages
st.subheader("Last 10 messages:")

while True:
    try:
        # Read and display the last 10 messages from the CSV file
        df = pd.read_csv('msg.csv')
        if not df.empty:
            for i, row in df.iterrows():
                st.write(f"{row['username']}: {row['message']}")
    except FileNotFoundError:
        st.write("No messages yet.")
    
    # Wait for 1 second and then refresh the messages
    time.sleep(1)
    st.experimental_rerun()
