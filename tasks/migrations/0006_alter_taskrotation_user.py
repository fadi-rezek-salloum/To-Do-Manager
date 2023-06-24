# Generated by Django 4.2.1 on 2023-05-11 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0005_alter_taskcompletion_task_alter_taskcompletion_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskrotation',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]