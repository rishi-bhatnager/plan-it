# Generated by Django 2.2.5 on 2020-03-06 03:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_task_addtime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='dueTime',
            new_name='dueDate',
        ),
        migrations.RemoveField(
            model_name='task',
            name='addTime',
        ),
        migrations.AddField(
            model_name='task',
            name='addDate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='time when task was added'),
        ),
        migrations.AlterField(
            model_name='task',
            name='expTime',
            field=models.DurationField(verbose_name='expected time for completion'),
        ),
    ]
