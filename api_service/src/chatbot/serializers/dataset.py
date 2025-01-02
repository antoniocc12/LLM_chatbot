from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from chatbot.models import Dataset, Topic
from chatbot.serializers.task import TaskMinSerializer


class DatasetSerializer(serializers.ModelSerializer):

    task = TaskMinSerializer(read_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'file', "task"]

    # noinspection PyMethodMayBeStatic
    def create(self, validated_data):
        request = self.context.get("request")
        view = self.context.get("view")
        if not validated_data.get("name"):
            validated_data["name"] = request.data.get("file").name
        validated_data["topic"] = get_object_or_404(Topic.objects.all(), slug=view.kwargs.get("slug"))
        validated_data["user_created"] = request.user
        return super().create(validated_data)
