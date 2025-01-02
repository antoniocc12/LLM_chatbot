from rest_framework import serializers

from chatbot.models import Task


class TaskSerializer(serializers.ModelSerializer):
    log_file = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "task_id", "queue", "kwargs", "status", "current_state", "result", "error", "log_file"]

    # noinspection PyMethodMayBeStatic
    def get_log_file(self, obj):
        if obj.log:
            return obj.log[len("/log/") + 1:]
        return obj.log


class TaskMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "task_id", "queue", "status", "current_state", "result"]
