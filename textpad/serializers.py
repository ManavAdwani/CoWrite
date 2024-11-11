from rest_framework import serializers
from .models import Documents

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
