from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from chatbot.models import Topic
from chatbot.serializers import TopicSerializer
from jobs.process_dataset.chroma_repository import delete_collection_data


class TopicList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopicSerializer
    queryset = Topic.objects.all().order_by('-id')


class TopicDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()
    lookup_field = "slug"

    def delete(self, request, slug, *args, **kwargs):
        delete_collection_data(collection=slug)
        return super().delete(request=request, slug=slug)
