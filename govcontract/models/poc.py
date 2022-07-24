from django.db import models

class PointOfContact(models.Model):
    id          = models.AutoField(primary_key=True)
    first_name  = models.CharField(max_length=64)
    last_name   = models.CharField(max_length=64)
    email       = models.EmailField()
    prefix      = models.CharField(max_length=16, null=True)
    title       = models.ForeignKey("Position", on_delete=models.CASCADE)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s. %s %s" % (self.prefix, self.first_name, self.last_name)

    class Meta:
        managed = True
