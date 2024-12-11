
from django.apps import AppConfig

class MinecraftConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'minecraft'

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
