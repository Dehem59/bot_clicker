from django.db import models


class Keyword(models.Model):

    nom = models.CharField(max_length=255, unique=True)

    @property
    def google_correspondance(self):
        correspondance = self.nom.rstrip().replace(" ", "+")
        return correspondance

    def __str__(self):
        return self.nom
