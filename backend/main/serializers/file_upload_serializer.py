from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    transcript = serializers.FileField(required=True)
    activity = serializers.FileField(required=False)
    receipt = serializers.FileField(required=False)
    