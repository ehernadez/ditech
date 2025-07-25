from rest_framework import serializers
from core.models import IntegrationTask

class IntegrationTaskSerializer(serializers.ModelSerializer):
    task_name = serializers.CharField(required=True)
    config = serializers.JSONField(required=True)

    class Meta:
        model = IntegrationTask
        fields = ['id', 'task_name', 'config', 'status', 'execution_time', 'result', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'execution_time', 'result', 'created_at', 'updated_at']