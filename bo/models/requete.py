from django.db import models

class Requete(models.Model):

    libelle = models.CharField(max_length=80)



