from django.db import models
from bo.models.requete import Requete

class SiteWeb(models.Model):

    url = models.TextField()
    requetes = models.ManyToManyField(Requete, blank=True, through="Aclicker")



