from django.db import models


class UserAgent(models.Model):

    nom = models.CharField(max_length=250)
    definition = models.TextField()

    def __str__(self):
        return self.nom
