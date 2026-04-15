
function toggleChat() {
    const popup = document.getElementById("chatPopup");
    popup.classList.toggle("active");
}

function sendMessage() {
    let input = document.getElementById("userInput");
    let message = input.value;

    if (!message) return;

    let chatBox = document.getElementById("chatBox");

    chatBox.innerHTML += `<div class="message user"> ${message}</div>`;

    fetch("/ai-chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        chatBox.innerHTML += `<div class="message ai">${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    input.value = "";
}
function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}
