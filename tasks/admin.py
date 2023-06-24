from django.contrib import admin

from .models import Task, TaskCompletion, TaskRotation, Category

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(TaskCompletion)
admin.site.register(TaskRotation)