from django.urls import path
from .views import TaskCreateView, TaskRotationCreateView, TaskListView, TaskCompleteView

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('rotation/create/', TaskRotationCreateView.as_view(), name='task_rotation_create'),
    path('list/<str:category>/', TaskListView.as_view(), name='task_list'),
    path('complete/<id>/', TaskCompleteView.as_view(), name='task_complete'),
]