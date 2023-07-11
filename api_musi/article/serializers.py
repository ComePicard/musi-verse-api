from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'creation_date', 'last_update']
        read_only_fields = ['id', 'creation_date', 'last_update']
