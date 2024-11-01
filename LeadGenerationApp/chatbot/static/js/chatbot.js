let lastUserInput = "";

async function handleSubmit(e) {
    e.preventDefault();
    const userInput = document.getElementById("user-input").value.trim();
    const errorMessage = document.getElementById("error-message");
    const spinner = document.getElementById("loading-spinner");

    if (errorMessage.textContent !== "") return;

    lastUserInput = userInput;
    document.getElementById("user-input").value = "";
    errorMessage.textContent = "";
    spinner.style.display = "block";

    try {
        const response = await fetch("{% url 'chatbot_interaction' %}", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": "{{ csrf_token }}",
            },
            body: new URLSearchParams({ user_input: userInput }),
        });
        const data = await response.json();

        document.getElementById("chat-log").innerHTML += `<p>Bot: ${data.bot_reply}</p>`;

        if (data.query) {
            document.getElementById("chat-log").innerHTML += `<p>Query: ${data.query}</p>`;
            document.getElementById("chat-log").innerHTML += `<p>You can type 'confirm' to proceed or edit the query directly.</p>`;
        }
    } catch (error) {
        console.error("Error fetching response:", error);
        errorMessage.textContent = "Network error. Please check your connection or try again.";
        errorMessage.classList.add("show");
    } finally {
        spinner.style.display = "none";
    }
}

document.getElementById("chat-form").addEventListener("submit", handleSubmit);


document.getElementById("chat-form").onsubmit = function (e) {
    e.preventDefault();

    const userInput = document.getElementById("user-input");
    const userMessage = userInput.value.trim();
    if (userMessage === "") return;

    // Add the user's message to the chat log
    const chatLog = document.getElementById("chat-log");
    const userMessageDiv = document.createElement("div");
    userMessageDiv.classList.add("chat-message", "user-message");
    userMessageDiv.innerHTML = `<p><strong>You:</strong> ${userMessage}</p>`;
    chatLog.appendChild(userMessageDiv);

    // Clear input field
    userInput.value = "";

    // Display loading spinner
    document.getElementById("loading-spinner").style.display = "block";

    // Send the form data with AJAX
    fetch("/chatbot_interaction/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        },
        body: new URLSearchParams({
            "user_input": userMessage
        })
    })
    .then(response => response.text())
    .then(responseText => {
        // Parse the response and add to chat log
        const botMessageDiv = document.createElement("div");
        botMessageDiv.classList.add("chat-message", "bot-message");
        botMessageDiv.innerHTML = `<p><strong>Bot:</strong> ${responseText}</p>`;
        chatLog.appendChild(botMessageDiv);

        // Hide loading spinner
        document.getElementById("loading-spinner").style.display = "none";

        // Scroll to the bottom of chat log
        chatLog.scrollTop = chatLog.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
    });
};