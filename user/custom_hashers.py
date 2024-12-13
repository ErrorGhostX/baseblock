import bcrypt
from django.contrib.auth.hashers import BasePasswordHasher
from django.core.exceptions import ValidationError

class BCrypt2aPasswordHasher(BasePasswordHasher):
    """
    Кастомный хешер для bcrypt2a с итерациями 10.
    """
    algorithm = "bcrypt2a"
    iterations = 10

    def salt(self):
        # Генерируем соль для bcrypt с нужным количеством итераций
        return bcrypt.gensalt(rounds=self.iterations)

    def encode(self, password, salt):
        # Применяем префикс 2a, если соль использует версию 2b
        if salt.startswith(b"$2b$"):
            salt = b"$2a$" + salt[4:]
        # Хешируем пароль с солью и возвращаем результат
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify(self, password, encoded):
        # Проверяем совпадение пароля с сохранённым хешом
        return bcrypt.checkpw(password.encode('utf-8'), encoded.encode('utf-8'))

    def safe_summary(self, encoded):
        # Возвращаем информацию о хеше для безопасного отображения
        return {
            'algorithm': self.algorithm,
            'iterations': self.iterations,
        }
