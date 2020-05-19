# Generated by Django 3.0.4 on 2020-05-17 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0009_auto_20200514_2128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'get_latest_by': ['addDate', 'dueDate'], 'ordering': ['name', 'notes', 'category', 'user', 'addDate', 'dueDate', 'expTime']},
        ),
        migrations.AddField(
            model_name='task',
            name='notes',
            field=models.TextField(default='', help_text='Notes'),
        ),
        migrations.AlterField(
            model_name='scheduleinstance',
            name='effective',
            field=models.BooleanField(default=None, verbose_name='Whether this instance was scheduled effectively'),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('Ex', 'Exercise'), ('Leis', 'Leisure'), ('House', 'Household'), ('Pers', 'Personal'), ('Work', 'Work'), ('', 'None')], default='', max_length=5),
        ),
        migrations.AlterUniqueTogether(
            name='scheduleinstance',
            unique_together={('startTime',)},
        ),
    ]