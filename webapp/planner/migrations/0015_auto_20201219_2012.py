# Generated by Django 3.0.3 on 2020-12-19 20:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0014_auto_20201219_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='addDate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Time When Block was Created'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Block Name'),
        ),
        migrations.AlterField(
            model_name='task',
            name='addDate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Time When Block was Created'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Block Name'),
        ),
    ]