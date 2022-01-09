from django.db import models
from django.utils import timezone
from bo.models.requete import Requete
from bo.models.siteweb import SiteWeb


class Aclicker(models.Model):
    requete = models.ForeignKey(Requete, null=True, on_delete=models.SET_NULL)
    siteweb = models.ForeignKey(SiteWeb, null=True, on_delete=models.SET_NULL)
    resultat = models.CharField(max_length=50)
    date_heure = models.DateTimeField(default=timezone.now)
    proxy = models.CharField(max_length=100)
    timescrolling = models.IntegerField()
    positition_page = models.IntegerField()






