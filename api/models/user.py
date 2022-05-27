from django.db import models


class UserModel(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = "api_users"

    def __str__(self):
        return self.first_name + " " + self.last_name
