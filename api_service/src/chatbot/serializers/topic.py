from django.utils.text import slugify
from rest_framework import serializers

from chatbot.models import Topic


class TopicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug', 'description']
        read_only_fields = ['id', 'slug']

    # noinspection PyMethodMayBeStatic
    def create(self, validated_data):
        validated_data["user_created"] = self.context.get("request").user
        return super().create(validated_data)
