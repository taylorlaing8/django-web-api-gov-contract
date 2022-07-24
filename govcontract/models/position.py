from django.db import models

class Position(models.Model):
    id          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=256)
    department  = models.CharField(max_length=256)
    created     = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
