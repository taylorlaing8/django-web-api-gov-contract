# Generated by Django 4.0.4 on 2022-07-02 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('govcontract', '0030_contract_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='bus_days',
            field=models.FloatField(default=0),
        ),
    ]
