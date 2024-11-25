import streamlit as st
import pandas as pd
import time
import os

# Function to read and update CSV file with new messages
def update_messages(message, username):
    # Read existing messages if the file exists
    if os.path.exists('msg.csv') and os.stat('msg.csv').st_size > 0:
        df = pd.read_csv('msg.csv')
    else:
        # Create an empty DataFrame if the file doesn't exist or is empty
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

# Using st.empty to refresh the message display
message_container = st.empty()

# Set up a refresh every second
while True:
    try:
        # Read and display the last 10 messages from the CSV file
        if os.path.exists('msg.csv'):
            df = pd.read_csv('msg.csv')
            if not df.empty:
                message_container.empty()  # Clear the previous messages
                for i, row in df.iterrows():
                    message_container.write(f"{row['username']}: {row['message']}")
            else:
                message_container.write("No messages yet.")
        else:
            message_container.write("No messages yet.")
        
        # Wait for 1 second before refreshing
        time.sleep(1)
    except Exception as e:
        message_container.write(f"Error: {str(e)}")
