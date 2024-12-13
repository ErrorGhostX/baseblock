# user/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from user.models import Profile
from django.contrib.auth.hashers import check_password
import bcrypt

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            from django.db import connection
            cursor = connection.cursor()

            # Получаем хешированный пароль из базы данных auth (Minecraft)
            cursor.execute("SELECT HASH FROM baseblock.auth WHERE NICKNAME = %s", [instance.username])
            result = cursor.fetchone()

            if result:
                hashed_password = result[0]  # Это зашифрованный пароль

                # Проверяем пароль с помощью bcrypt
                if bcrypt.checkpw(instance.password.encode('utf-8'), hashed_password.encode('utf-8')):
                    # Если пароль совпадает, создаем профиль
                    Profile.objects.create(
                        user=instance,
                        description="Описание отсутствует",
                        city="Не указан",
                        social_rating=0
                    )
        except Exception as e:
            print(f"Ошибка при создании профиля: {e}")
