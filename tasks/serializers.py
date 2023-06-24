from rest_framework import serializers
from .models import Task, TaskRotation, TaskCompletion, Category

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCompletion
        fields = '__all__'

class TaskRotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRotation
        fields = '__all__'
