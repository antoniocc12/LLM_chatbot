from rest_framework import status
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chatbot.models import Topic, History
from chatbot.serializers import HistorySerializer


class HistoryList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HistorySerializer
    queryset = History.objects.order_by('-id')

    def get_history(self):
        topic = get_object_or_404(Topic.objects.all(), slug=self.kwargs["slug"])
        return self.queryset.filter(topic=topic, user_created=self.request.user)

    def get_queryset(self):
        return self.get_history().all()[:5:-1]

    def delete(self, request, *args, **kwargs):
        self.get_history().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
