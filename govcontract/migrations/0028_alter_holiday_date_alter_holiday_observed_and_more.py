# Generated by Django 4.0.4 on 2022-06-28 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('govcontract', '0027_remove_task_updated_task_status_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='observed',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='ssp_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(),
        ),
    ]
