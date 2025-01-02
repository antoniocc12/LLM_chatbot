from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('chatbot/', include('chatbot.urls', namespace='chatbot')),
]