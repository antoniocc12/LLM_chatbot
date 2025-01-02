from rest_framework.response import Response
from rest_framework.views import APIView

from chatbot.serializers import UserSerializer


class WhoAmI(APIView):
    # noinspection PyMethodMayBeStatic,PyUnusedLocal,PyShadowingBuiltins
    def get(self, request, format=None):
        user = None
        is_authenticated = False
        username = "guest"
        if request.user and request.user.is_authenticated:
            user = UserSerializer(request.user).data
            is_authenticated = True
            username = request.user.username
        return Response(data={
            "message": f"You are {username}.",
            "is_authenticated": is_authenticated,
            "user": user,
        })
