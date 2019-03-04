from .models import Nugget
from rest_framework import serializers


class NuggetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nugget
        fields = ('id', 'creator', 'source', 'content', 'created_at', 'updated_at', 'deleted_at')
