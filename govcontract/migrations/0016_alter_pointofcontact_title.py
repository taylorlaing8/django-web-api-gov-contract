# Generated by Django 4.0.4 on 2022-06-20 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('govcontract', '0015_alter_contract_id_alter_pointofcontact_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointofcontact',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='govcontract.position'),
        ),
    ]
