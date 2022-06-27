from django.db import models
from .status import Status

class Contract(models.Model):
    id          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=255)
    sub_title   = models.CharField(max_length=255, null=True)
    slug        = models.CharField(max_length=255)
    type        = models.CharField(max_length=55)
    ucid        = models.CharField(max_length=55)   # Unique Contract ID
    status      = models.CharField(max_length=2, choices=Status.choices, default=Status.INCOMPLETE)
    value       = models.FloatField()               # In millions of dollars (i.e. 455.53 = $455.53M)
    ss_leads    = models.ManyToManyField('PointOfContact', related_name="ss_leads")
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
    pocs        = models.ManyToManyField('PointOfContact', related_name="pocs")
    created     = models.DateTimeField(auto_now_add=True)
