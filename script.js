document.getElementById("messageForm").addEventListener("submit", async function(event) {
  event.preventDefault();

  const message = document.getElementById("message").value;

  // Send the message to the Netlify function via an API call
  try {
    const response = await fetch("/.netlify/functions/ftp-messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    console.log("Message sent:", data);

    // Refresh the messages after sending
    await loadMessages();
  } catch (error) {
    console.error("Error sending message:", error);
  }
});

async function loadMessages() {
  try {
    const response = await fetch("/.netlify/functions/ftp-messages");
    const data = await response.json();

    const messageList = document.getElementById("messageList");
    messageList.innerHTML = data.messages.replace(/\n/g, "<br>");
  } catch (error) {
    console.error("Error loading messages:", error);
  }
}

// Load messages on page load
loadMessages();
