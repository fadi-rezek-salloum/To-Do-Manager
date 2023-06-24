from accounts.models import User
from django.utils import timezone
from rest_framework import generics, permissions

from .models import Category, Task, TaskCompletion, TaskRotation
from .serializers import (TaskCompletionSerializer, TaskRotationSerializer,
                          TaskSerializer)


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            rotation = TaskRotation.objects.get(user=self.request.user)
            day = ((timezone.now().date() - rotation.start_date).days + 1) % rotation.max_rotation

            if day == 0:
                day = rotation.max_rotation
            
            category = Category.objects.get(name__icontains=self.request.data.get('category_text'))
            user = self.request.user

            serializer.validated_data['category'] = category
            serializer.validated_data['user'] = user
            serializer.validated_data['day_number'] = day

            instance = serializer.save()

            rotation.tasks.add(instance)

        else:
            category = Category.objects.get(name__icontains=self.request.data.get('category_text'))
            user = self.request.user

            serializer.validated_data['category'] = category
            serializer.validated_data['user'] = user

            serializer.save()


class TaskRotationCreateView(generics.CreateAPIView):
    serializer_class = TaskRotationSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def perform_create(self, serializer):
        user = User.objects.get(email=self.request.data.get('email'))
        category = Category.objects.get(name__icontains=self.request.data.get('category'))
        
        serializer.validated_data['user'] = user

        instance = serializer.save()
        
        tasks = Task.objects.filter(user__is_staff=True, category=category)

        instance.tasks.set(tasks)

        
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_queryset(self):
        category = Category.objects.get(name__icontains=self.kwargs['category'])

        tasks_rotation = (TaskRotation.objects.filter(user=self.request.user, start_date__lte=timezone.now().date(), tasks__category=category) | TaskRotation.objects.filter(tasks__user__is_superuser=True, start_date__lte=timezone.now().date(), tasks__category=category)).distinct()

        tasks_ids = tasks_rotation.values_list('tasks__id', flat=True)

        day = ((timezone.now().date() - tasks_rotation.first().start_date).days + 1) % tasks_rotation.first().max_rotation

        if day == 0:
            day = tasks_rotation.first().max_rotation

        print(day)

        tasks = Task.objects.filter(pk__in=tasks_ids, day_number=day)

        return tasks


class TaskCompleteView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskCompletionSerializer

    def perform_create(self, serializer):
        task = Task.objects.get(id=self.kwargs.get('id'))
        user = self.request.user

        serializer.validated_data['task'] = task
        serializer.validated_data['user'] = user
        serializer.validated_data['is_completed'] = True

        serializer.save()
