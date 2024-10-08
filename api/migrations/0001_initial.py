# Generated by Django 4.0.4 on 2022-05-28 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255)),
                ("created", models.DateField(auto_now_add=True)),
            ],
            options={
                "db_table": "api_users",
                "managed": True,
            },
        ),
    ]
