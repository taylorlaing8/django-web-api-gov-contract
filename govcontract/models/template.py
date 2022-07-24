from django.db import models

class Template(models.Model):
    id          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=256)
    sub_title   = models.CharField(max_length=256, null=True)
    data        = models.JSONField()
    created     = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
