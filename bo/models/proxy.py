from django.db import models


class Proxy(models.Model):

    host = models.GenericIPAddressField(verbose_name="Proxy Host", unique=True)
    port = models.CharField(max_length=8)
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.host}:{self.port}"
