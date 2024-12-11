import ollama
import json
import os
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

# Загрузка контекста из файла
def load_context():
    context_path = os.path.join(os.path.dirname(__file__), "./static/minecraft/context.json")
    try:
        with open(context_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data["context"]
    except FileNotFoundError:
        return "Контекст не найден"


# Генерация ответа с учетом контекста
def generate_response(prompt, chat_history):
    context = load_context()
    # Ограничиваем историю чата до последних 5 сообщений
    history_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history[-5:]])  # Используем последние 5 сообщений
    full_prompt = f"{context}\n\n{history_prompt}\n\n{prompt}"  # Контекст + история + текущее сообщение

    # Генерация ответа от модели
    try:
        stream = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": full_prompt}],
            stream=True,
        )
        for chunk in stream:
            yield chunk["message"]["content"]
    except Exception as e:
        yield f"Произошла ошибка при генерации ответа: {str(e)}"


@csrf_exempt
def chat_view(request):
    # Используем сессию для хранения истории чата
    if "chat_history" not in request.session:
        request.session["chat_history"] = []  # Инициализация истории, если её нет в сессии

    if request.method == "POST":
        user_input = request.POST.get("user_input")
        if not user_input:
            return StreamingHttpResponse("Ошибка: сообщение отсутствует.", content_type="text/plain")

        # Добавляем новое сообщение в историю
        chat_history = request.session["chat_history"]
        chat_history.append({"role": "user", "content": user_input})

        # Ограничиваем количество сообщений в истории до 5
        if len(chat_history) > 5:
            chat_history.pop(0)  # Убираем старые сообщения

        # Сохраняем обновленную историю в сессию
        request.session["chat_history"] = chat_history

        def response_stream():
            try:
                for chunk in generate_response(user_input, chat_history):
                    yield chunk
            except Exception as e:
                yield f"Ошибка при отправке сообщения: {str(e)}"

        return StreamingHttpResponse(response_stream(), content_type="text/plain")

    return render(request, "minecraft/chat.html")
