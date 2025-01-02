from rest_framework import serializers

from chatbot.models import History


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = ['id', 'query', 'answer', 'metadata']
