# Generated by Django 4.0.4 on 2022-06-28 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('govcontract', '0026_alter_task_palt_actual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='updated',
        ),
        migrations.AddField(
            model_name='task',
            name='status_updated',
            field=models.DateTimeField(null=True),
        ),
    ]
