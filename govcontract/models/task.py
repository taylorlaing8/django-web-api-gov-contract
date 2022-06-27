from django.db import models
from .status import Status

class Task(models.Model):
    id          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=255)
    sub_title   = models.CharField(max_length=255, null=True)
    slug        = models.CharField(max_length=255)
    status      = models.CharField(max_length=2, choices=Status.choices, default=Status.INCOMPLETE)
    task_id     = models.ForeignKey("Task", on_delete=models.CASCADE, null=True)
    contract_id = models.ForeignKey("Contract", on_delete=models.CASCADE, related_name="contract_id")
    order_id    = models.IntegerField()
    gate        = models.IntegerField()
    sub_gate    = models.IntegerField(null=True)
    palt_plan   = models.FloatField()
    bus_days    = models.FloatField(null=True)
    start_date  = models.DateTimeField()
    end_date    = models.DateTimeField()
    ssp_date    = models.DateTimeField(null=True)
    poc         = models.ForeignKey("PointOfContact", on_delete=models.CASCADE, related_name="poc", null=True)
    comments    = models.CharField(max_length=500, null=True)
    created     = models.DateTimeField(auto_now_add=True)

    @property
    def palt_actual(self):
        return self.end_date - self.start_date
