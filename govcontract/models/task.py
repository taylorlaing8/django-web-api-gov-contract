from django.db import models
from .status import Status

class Task(models.Model):
    id          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=256)
    sub_title   = models.CharField(max_length=256, null=True)
    slug        = models.CharField(max_length=256)
    status      = models.CharField(max_length=2, choices=Status.choices, default=Status.INCOMPLETE)
    task_id     = models.ForeignKey("Task", on_delete=models.CASCADE, null=True)
    contract_id = models.ForeignKey("Contract", on_delete=models.CASCADE, related_name="contract_id")
    order_id    = models.IntegerField()
    gate        = models.IntegerField()
    sub_gate    = models.IntegerField(null=True)
    palt_plan   = models.FloatField()
    palt_actual = models.IntegerField()
    bus_days    = models.FloatField(default=0)
    start_date  = models.DateField()
    end_date    = models.DateField()
    ssp_date    = models.DateField(null=True)
    poc         = models.ForeignKey("PointOfContact", on_delete=models.CASCADE, related_name="poc", null=True)
    comments    = models.CharField(max_length=1024, null=True)
    links       = models.JSONField(null=True)
    created     = models.DateTimeField(auto_now_add=True)
    status_updated     = models.DateTimeField()

    def get_all_tasks(self):
        return Task.objects.filter(task_id=self.id).order_by('order_id')

    class Meta:
        managed = True
