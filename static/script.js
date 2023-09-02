// JavaScript code for handling conversation and messages
document.addEventListener('DOMContentLoaded', function () {
    const conversationContainer = document.getElementById('conversation-container');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    function addMessage(text, messageType) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', messageType);
        messageElement.textContent = text;
        conversationContainer.appendChild(messageElement);
        
        // Scroll to the bottom of the conversation container to show new messages
        conversationContainer.scrollTop = conversationContainer.scrollHeight;
    }

    sendButton.addEventListener('click', () => {
        const message = messageInput.value.trim();
        if (message !== '') {
            addMessage(message, 'user-message');
            messageInput.value = '';

            // Send the user's message to the server (you'll implement this in Flask)
            sendMessageToServer(message);
        }
    });

    function sendMessageToServer(message) {
        // Send an HTTP POST request to the server with the user's message
        fetch('/forward', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `message=${encodeURIComponent(message)}`,
        })
        .then(response => response.json())
        .then(data => {
            // Receive and display the server's answer
            const answer = data.answer;
            addMessage(answer, 'bot-message');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
