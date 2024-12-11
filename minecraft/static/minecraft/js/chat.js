$(document).ready(function() {
    const chatbox = $("#chatbox");
    const chatForm = $("#chat-form");
    const userInput = $("#user-input");
    let chatHistory = []; // Массив для хранения истории сообщений

    // Загружаем историю чата из сессии (из localStorage или другого источника)
    // Однако мы не сохраняем ее в localStorage, это будет делать сервер

    chatForm.submit(function(event) {
        event.preventDefault();
        const message = userInput.val().trim();
        if (!message) return;

        // Добавляем сообщение пользователя в чат
        appendMessage("Вы", message, "text-yellow");
        chatHistory.push({"role": "user", "content": message});

        // Отправляем сообщение на сервер с историей
        $.ajax({
            url: chatUrl,
            type: "POST",
            data: {
                user_input: message,
                chat_history: JSON.stringify(chatHistory) // Отправляем историю чата
            },
            xhrFields: {
                onprogress: function(event) {
                    const chunk = event.target.responseText;
                    const aiResponseElement = $("<p>");
                    chatbox.append($("<strong>").text("BaseBlockAI:").css("color", "purple"));
                    chatbox.append(aiResponseElement);
                    aiResponseElement.html(chunk);
                    chatbox.scrollTop(chatbox[0].scrollHeight);
                }
            },
            success: function(response) {
                console.log("Сообщение успешно отправлено");
            },
            error: function() {
                console.error("Ошибка: не удалось получить ответ.");
            }
        });
    });

    // Функция добавления сообщений в чат
    function appendMessage(role, content, className) {
        chatbox.append(`<p class="${className}"><strong>${role}:</strong> ${content}</p>`);
        chatbox.scrollTop(chatbox[0].scrollHeight);
    }
});
