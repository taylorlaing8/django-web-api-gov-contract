# Generated by Django 4.0.4 on 2022-07-13 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('govcontract', '0035_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='links',
            field=models.ManyToManyField(related_name='links', to='govcontract.file'),
        ),
    ]
