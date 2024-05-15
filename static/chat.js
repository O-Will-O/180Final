function sendMessage() {
    var messageInput = document.getElementById('messageInput');
    var message = messageInput.value.trim();
    if (message !== '') {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/send', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                messageInput.value = '';
                fetchMessages();
            }
        };
        xhr.send(JSON.stringify({
            sender: 'Customer1', 
            recipient: 'Admin1', 
            content: message
        }));
    }
}

function fetchMessages() {
    var chatbox = document.getElementById('chatbox');
    chatbox.innerHTML = '';
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/messages?sender=Customer1&recipient=Admin1', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            var messages = JSON.parse(xhr.responseText);
            messages.forEach(function (message) {
                var messageDiv = document.createElement('div');
                messageDiv.textContent = message.Content;
                chatbox.appendChild(messageDiv);
            });
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    };
    xhr.send();
}

fetchMessages();
setInterval(fetchMessages, 5000); // Fetch messages every 5 seconds