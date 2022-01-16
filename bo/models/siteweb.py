from django.db import models
from bo.models.requete import Requete

class SiteWeb(models.Model):

    url = models.TextField()
    requetes = models.ManyToManyField(Requete, blank=True, through="Aclicker")

    def __str__(self):
        return self.url

    class Meta:
        verbose_name_plural = "URL cliquées"
        verbose_name = "URL cliquée"

