from django.db import models

class Requete(models.Model):

    libelle = models.CharField(max_length=80)

    def __str__(self):
        return self.libelle



