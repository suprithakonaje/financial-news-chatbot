document.addEventListener("DOMContentLoaded", () => {
    const queryInput = document.getElementById("query");
    const chatHistory = document.getElementById("chat-history");
    const askButton = document.getElementById("ask-button");
    const modeSelect = document.getElementById("mode");

    const handleAsk = async () => {
        const query = queryInput.value.trim();
        const mode = modeSelect.value;

        if (!query) return;

        queryInput.disabled = true;
        askButton.disabled = true;
        askButton.innerText = "Loading...";

        // Display user message
        const userDiv = document.createElement("div");
        userDiv.className = "p-3 rounded-lg bg-blue-600 text-white self-end max-w-[80%] break-words";
        userDiv.innerHTML = `<p>${query}</p>`;
        chatHistory.appendChild(userDiv);

        // Placeholder bot message
        const botDiv = document.createElement("div");
        botDiv.className = "p-3 rounded-lg bg-gray-700 text-white max-w-[80%] break-words animate-pulse";
        botDiv.innerHTML = `<p>Thinking...</p>`;
        chatHistory.appendChild(botDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        try {
            const res = await fetch("/ask", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({query, mode})
            });
            const data = await res.json();

            botDiv.classList.remove("animate-pulse");
            botDiv.innerHTML = `
                <p class="font-bold mb-2">Bot's Response (${mode}):</p>
                <p>${data.answer}</p>
            `;

            if (data.sources && data.sources.length > 0) {
                const sourcesDiv = document.createElement("div");
                sourcesDiv.className = "text-sm text-gray-400 mt-2 border-t border-gray-600 pt-2";
                let html = '<p class="font-semibold mb-1">Sources:</p>';
                data.sources.forEach((s, i) => {
                    html += `<p class="truncate"><a href="${s.link}" target="_blank" class="text-blue-400 hover:underline">Source ${i + 1}</a>: ${s.title}</p>`;
                });
                sourcesDiv.innerHTML = html;
                botDiv.appendChild(sourcesDiv);
            }

        } catch (err) {
            botDiv.classList.remove("animate-pulse");
            botDiv.innerHTML = `<p class="text-red-400">Error: ${err.message}</p>`;
        } finally {
            queryInput.disabled = false;
            askButton.disabled = false;
            askButton.innerText = "Ask";
            queryInput.value = "";
            queryInput.focus();
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    };

    askButton.addEventListener("click", handleAsk);
    queryInput.addEventListener("keydown", (e) => { if(e.key === "Enter") handleAsk(); });
});
