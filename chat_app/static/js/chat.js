document.addEventListener("DOMContentLoaded", function () {
    // Get the room name from the hidden input field
    const roomInput = document.getElementById("room-name");
    if (!roomInput) {
        console.error("Room name element not found in the DOM.");
        return;
    }
    const roomName = roomInput.value;

    // Determine the WebSocket protocol based on the page's protocol
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const chatSocket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/${roomName}/`);

    // Handle incoming WebSocket messages
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        if (data.type === "message") {
            const messageHTML = `<li><strong>${data.username}:</strong> ${data.message}</li>`;
            const messagesElement = document.querySelector("#messages");
            if (messagesElement) {
                messagesElement.innerHTML += messageHTML;
                document.querySelector("#no-messages").style.display = "none";
            }
        }

        if (data.type === "user_list") {
            const userListElement = document.querySelector("#user-list");
            if (userListElement) {
                userListElement.innerHTML = "";
                if (data.users.length === 0) {
                    document.querySelector("#no-users").style.display = "block";
                } else {
                    data.users.forEach((user) => {
                        const userElement = `<li>${user}</li>`;
                        userListElement.innerHTML += userElement;
                    });
                    document.querySelector("#no-users").style.display = "none";
                }
            }
        }
    };

    // Handle WebSocket closure
    chatSocket.onclose = function () {
        console.error("WebSocket closed unexpectedly.");
    };

    // Function to send messages
    window.sendMessage = function () {
        const input = document.querySelector("#messageInput");
        if (input && chatSocket.readyState === WebSocket.OPEN) {
            const message = input.value;
            if (message) {
                chatSocket.send(JSON.stringify({ message }));
                input.value = ""; // Clear the input field after sending
            }
        } else {
            console.error("Chat socket not initialized or not open.");
        }
    };

    // Function to leave the room
    window.leaveRoom = function () {
        window.location.href = "/";
    };

    // Fetch chat history on page load
    fetch(`/history/${roomName}/`)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Error loading chat history.");
            }
            return response.json();
        })
        .then((data) => {
            const messagesElement = document.querySelector("#messages");
            if (messagesElement && data.messages.length > 0) {
                data.messages.forEach((msg) => {
                    const messageHTML = `<li><strong>${msg.username}:</strong> ${msg.message} <em>(${msg.timestamp})</em></li>`;
                    messagesElement.innerHTML += messageHTML;
                });
                document.querySelector("#no-messages").style.display = "none";
            }
        })
        .catch((error) => {
            console.error("Error Fetching Chat History:", error);
            const messagesElement = document.querySelector("#messages");
            if (messagesElement) {
                messagesElement.innerHTML = `<li style="color: red;">Failed to load chat history. Please try again later.</li>`;
            }
        });
});
