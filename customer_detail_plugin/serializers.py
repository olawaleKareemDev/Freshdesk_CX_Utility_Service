from rest_framework import serializers


class CustomerSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)