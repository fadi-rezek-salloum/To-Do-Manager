from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    description = models.TextField()

    day_number = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.description
    
    
class TaskCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True)

    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + ' ' + str(self.task.id)
    

    
class TaskRotation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)

    current_rotation = models.PositiveSmallIntegerField(default=1)
    max_rotation = models.PositiveSmallIntegerField(default=7)

    start_date = models.DateField()
    
    tasks = models.ManyToManyField(Task, blank=True)

    def __str__(self):
        return self.user.email
    