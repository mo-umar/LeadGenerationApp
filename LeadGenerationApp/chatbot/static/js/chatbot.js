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
