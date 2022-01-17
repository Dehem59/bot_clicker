from django.db import models


class Proxy(models.Model):

    host = models.GenericIPAddressField(verbose_name="Proxy Host", unique=True)
    port = models.CharField(max_length=8)
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    est_actif = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['host', 'password'], name='unique_host_password_couple')
        ]

    def __str__(self):
        return f"{self.host}:{self.port}"
