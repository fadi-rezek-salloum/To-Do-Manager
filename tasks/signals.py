from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskRotation, TaskCompletion

@receiver(post_save, sender=TaskCompletion)
def check_task_rotation_completion(sender, instance, **kwargs):
    task_rotation = TaskRotation.objects.get(user=instance.user)
    tasks = task_rotation.tasks.all()

    all_completed = all(task.taskcompletion_set.filter(is_completed=True).exists() for task in tasks)

    if all_completed:
        task_rotation.current_rotation += 1
        task_rotation.save()
        task_completion_queryset = TaskCompletion.objects.filter(task__in=tasks, user=task_rotation.user)
        task_completion_queryset.delete()

    if task_rotation.current_rotation == task_rotation.max_rotation:
        task_rotation.delete()