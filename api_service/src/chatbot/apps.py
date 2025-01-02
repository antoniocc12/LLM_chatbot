from django.apps import AppConfig

from init_models import load_models


class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'

    load_models()
