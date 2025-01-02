from rest_framework import serializers


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, allow_null=False, max_length=5000, allow_blank=False)
