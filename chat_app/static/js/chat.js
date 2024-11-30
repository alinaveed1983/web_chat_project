const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#messages').innerHTML += `<li><strong>${data.username}:</strong> ${data.message}</li>`;
};

function sendMessage() {
    const input = document.querySelector('#messageInput');
    const message = input.value;
    chatSocket.send(JSON.stringify({ 'message': message }));
    input.value = '';
}
