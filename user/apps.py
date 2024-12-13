from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    def ready(self):
        from user.views import import_users_from_auth

        # Импортируем пользователей при запуске приложения
        import_users_from_auth()





