from http import HTTPStatus

import bcrypt
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

import json
import os
from django.test import TestCase, Client
from django.urls import reverse
from django.http import StreamingHttpResponse
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse

import os
import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from django.http import StreamingHttpResponse

class ExistingUserLoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "ErrorGhostX"
        cls.password = "30-30-30"
        from django.contrib.auth import get_user_model
        user_model = get_user_model()
        hashed_password = bcrypt.hashpw(cls.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cls.user = user_model.objects.create(username=cls.username, password=hashed_password)

    def test_existing_user_login_success(self):
        response = self.client.post(reverse("login"), {
            "username": self.username,
            "password": self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/profile/{self.username}/')

    def test_existing_user_login_failure_invalid_password(self):
        response = self.client.post(reverse("login"), {
            "username": self.username,
            "password": "wrong_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(response.context["form"].non_field_errors()[0], "Неправильное имя пользователя или пароль")

    def test_existing_user_login_failure_invalid_username(self):
        response = self.client.post(reverse("login"), {
            "username": "WrongUsername",
            "password": self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(response.context["form"].non_field_errors()[0], "Неправильное имя пользователя или пароль")




class OllamaApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.chat_url = reverse("chat")  # Убедитесь, что этот путь настроен в urls.py
        self.context_path = os.path.join(os.path.dirname(__file__), "./static/minecraft/context.json")

        # Создаем фейковый контекст для тестов
        self.fake_context = {"context": "This is a test context."}
        os.makedirs(os.path.dirname(self.context_path), exist_ok=True)
        with open(self.context_path, "w", encoding="utf-8") as file:
            json.dump(self.fake_context, file)

    def tearDown(self):
        # Удаляем тестовый файл контекста
        if os.path.exists(self.context_path):
            os.remove(self.context_path)

    @patch("ollama.chat")
    def test_generate_response(self, mock_ollama_chat):
        # Настройка mock для ollama.chat
        mock_stream = MagicMock()
        mock_stream.__iter__.return_value = iter([
            {"message": {"content": "Test response chunk 1"}},
            {"message": {"content": "Test response chunk 2"}}
        ])
        mock_ollama_chat.return_value = mock_stream

        # Отправляем POST-запрос с данными пользователя
        response = self.client.post(self.chat_url, {"user_input": "Hello, Ollama!"})

        # Проверяем, что ответ является StreamingHttpResponse
        self.assertIsInstance(response, StreamingHttpResponse)

        # Проверяем содержимое стрима
        response_content = "".join([chunk.decode("utf-8") for chunk in response.streaming_content])
        self.assertIn("Test response chunk 1", response_content)
        self.assertIn("Test response chunk 2", response_content)

    def test_missing_user_input(self):
        # Отправляем запрос без пользовательского ввода
        response = self.client.post(self.chat_url, {"user_input": ""})

        # Проверяем, что возвращается ошибка
        response_content = "".join([chunk.decode("utf-8") for chunk in response.streaming_content])
        self.assertEqual(response_content, "Ошибка: сообщение отсутствует.")

    def test_chat_history_persistence(self):
        # Отправляем два сообщения подряд
        self.client.post(self.chat_url, {"user_input": "First message"})
        self.client.post(self.chat_url, {"user_input": "Second message"})

        # Проверяем, что история чата хранится в сессии
        session = self.client.session
        chat_history = session.get("chat_history", [])
        self.assertEqual(len(chat_history), 2)
        self.assertEqual(chat_history[0]["content"], "First message")
        self.assertEqual(chat_history[1]["content"], "Second message")

    def test_chat_history_limit(self):
        # Отправляем 6 сообщений
        for i in range(6):
            self.client.post(self.chat_url, {"user_input": f"Message {i+1}"})

        # Проверяем, что в истории хранится только 5 последних сообщений
        session = self.client.session
        chat_history = session.get("chat_history", [])
        self.assertEqual(len(chat_history), 5)
        self.assertEqual(chat_history[0]["content"], "Message 2")
        self.assertEqual(chat_history[-1]["content"], "Message 6")
