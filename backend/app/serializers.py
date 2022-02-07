from rest_framework import serializers


class PageSerializer(serializers.Serializer):
    title = serializers.CharField()

    class Meta:
        fields = ["title"]
