from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chatbot.serializers.query import QuerySerializer
from jobs.knowledge_retrieval.controller import start_knowledge_retrieval


class Query(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuerySerializer

    def post(self, request, slug, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query = serializer.data.get("query")
        print(f"received query request with topic {slug} and query {query}")
        try:
            response = start_knowledge_retrieval(topic=slug, query=query, user=request.user)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status.HTTP_200_OK)
