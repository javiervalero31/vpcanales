from django.db import models


class Imei(models.Model):
    imei = models.IntegerField()
    tecnologia = models.CharField(max_length=2, null=False)

    class Meta:
        verbose_name_plural = "Codigos IMEI"

    def __str__(self):
        return 'IMEI: ' + str(self.imei) + ', tecnologia: ' + self.tecnologia
