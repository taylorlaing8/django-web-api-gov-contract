from django.db import models
from django.utils.translation import gettext_lazy as _

class Status(models.TextChoices):
    INCOMPLETE = 'IC', _('Incomplete')
    INPROGRESS = 'IP', _('In Progress')
    COMPLETE = 'CP', _('Complete')
