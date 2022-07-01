from django.db import models

class Holiday(models.Model):
    id          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=255)
    details     = models.CharField(max_length=255, null=True)
    date        = models.DateField()
    observed    = models.DateField()

    class Meta:
        managed = True
