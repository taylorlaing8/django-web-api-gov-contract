# Generated by Django 4.0.4 on 2022-06-27 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('govcontract', '0018_alter_task_bus_days'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('details', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('observed', models.DateTimeField()),
            ],
        ),
    ]
