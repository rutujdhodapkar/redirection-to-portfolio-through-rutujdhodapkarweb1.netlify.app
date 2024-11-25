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

while True:
    try:
        # Read and display the last 10 messages from the CSV file
        if os.path.exists('msg.csv'):
            df = pd.read_csv('msg.csv')
            if not df.empty:
                for i, row in df.iterrows():
                    st.write(f"{row['username']}: {row['message']}")
            else:
                st.write("No messages yet.")
        else:
            st.write("No messages yet.")
    except Exception as e:
        st.write(f"Error reading messages: {str(e)}")
    
    # Wait for 1 second and then refresh the messages
    time.sleep(1)
    st.experimental_rerun()
