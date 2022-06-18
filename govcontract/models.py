from django.db import models
from datetime import datetime, timedelta
import numpy as np
from django.utils.translation import gettext_lazy as _

class Status(models.TextChoices):
    INCOMPLETE = 'IC', _('Incomplete')
    INPROGRESS = 'IP', _('In Progress')
    COMPLETE = 'CP', _('Complete')

class Position(models.Model):
    title       = models.CharField(max_length=255)
    department  = models.CharField(max_length=255)
    created     = models.DateTimeField(auto_now_add=True)

class PointOfContact(models.Model):
    first_name  = models.CharField(max_length=55)
    last_name   = models.CharField(max_length=55)
    email       = models.EmailField()
    prefix      = models.CharField(max_length=10, null=True)
    title       = models.ForeignKey("Position", on_delete=models.CASCADE)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s. %s %s" % (self.prefix, self.first_name, self.last_name)

class Contract(models.Model):
    title       = models.CharField(max_length=255)
    sub_title   = models.CharField(max_length=255, null=True)
    slug        = models.CharField(max_length=255)
    type        = models.CharField(max_length=55)
    ucid        = models.CharField(max_length=55)   # Unique Contract ID
    status      = models.CharField(max_length=2, choices=Status.choices, default=Status.INCOMPLETE)
    value       = models.FloatField()               # In millions of dollars (i.e. 455.53 = $455.53M)
    ss_lead_ids = models.ManyToManyField('PointOfContact', related_name="ss_lead_ids")
    need_date   = models.DateTimeField(null=True)
    award_date  = models.DateTimeField(null=True)
    pco         = models.ForeignKey("PointOfContact", on_delete=models.CASCADE, related_name="pco")             # POC field
    buyer       = models.ForeignKey("PointOfContact", on_delete=models.CASCADE, related_name="buyer")           # POC field
    admin_pco   = models.ForeignKey("PointOfContact", on_delete=models.CASCADE, related_name="admin_pco")       # POC field
    admin_buyer = models.ForeignKey("PointOfContact", on_delete=models.CASCADE, related_name="admin_buyer")     # POC field
    cycle_code  = models.CharField(max_length=55)
    pop_date    = models.DateTimeField(null=True)   # When current contract ends
    g_o_p       = models.IntegerField()
    g_t_p       = models.IntegerField()
    g_tr_p      = models.IntegerField()
    g_fr_o_p    = models.IntegerField()
    g_fr_t_p    = models.IntegerField()
    g_fr_tr_p   = models.IntegerField()
    g_fr_fr_p   = models.IntegerField()
    g_fr_fv_p   = models.IntegerField()
    poc_ids     = models.ManyToManyField('PointOfContact', related_name="poc_ids")
    created     = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    title       = models.CharField(max_length=255)
    sub_title   = models.CharField(max_length=255, null=True)
    slug        = models.CharField(max_length=255)
    status      = models.CharField(max_length=2, choices=Status.choices, default=Status.INCOMPLETE)
    # task_id     = models.ForeignKey("Task", on_delete=models.CASCADE)
    contract_id = models.ForeignKey("Contract", on_delete=models.CASCADE)
    order_id    = models.IntegerField()
    gate        = models.IntegerField()
    sub_gate    = models.IntegerField(null=True)
    palt_plan   = models.FloatField()
    bus_days    = models.IntegerField(null=True)
    start_date  = models.DateTimeField()
    end_date    = models.DateTimeField()
    ssp_date    = models.DateTimeField(null=True)
    poc         = models.ForeignKey("PointOfContact", on_delete=models.CASCADE, null=True)
    comments    = models.CharField(max_length=500, null=True)
    tasks       = models.ManyToManyField('Task')
    created     = models.DateTimeField(auto_now_add=True)

    @property
    def palt_actual(self):
        return self.end_date - self.start_date
    
    # @property
    # def bus_days(self):
    #     return np.busday_count(self.start_date.strftime('%Y-%m-%d'), self.end_date.strftime('%Y-%m-%d'))

    # def __str__(self):
    #     return "%s (%s)" % (self.title, self.sub_title)