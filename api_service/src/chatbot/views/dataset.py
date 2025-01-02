from rest_framework import status
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chatbot.models import Dataset, Topic, Task
from chatbot.serializers import DatasetSerializer
from jobs.process_dataset.process_dataset import process_dataset_task


class DatasetList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all().order_by('-id')

    def get_queryset(self):
        queryset = super().get_queryset()
        topic = get_object_or_404(Topic.objects.all(), slug=self.kwargs["slug"])
        return queryset.filter(topic=topic)

    def create(self, request, *args, **kwargs):
        response_data = super().create(request, *args, **kwargs).data
        dataset_id = response_data.get("id")
        dataset = Dataset.objects.get(id=dataset_id)

        queue = "process_dataset_queue"
        task_kwargs = {"dataset_id": dataset_id}
        result = process_dataset_task.apply_async(queue=queue, kwargs=task_kwargs)

        dataset.task = Task.objects.create(task_id=result.task_id, queue=queue, kwargs=task_kwargs)
        dataset.save()
        return Response(self.get_serializer(dataset).data, status=status.HTTP_202_ACCEPTED)
