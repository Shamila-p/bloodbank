from django.db import models

# Create your models here.


class Donor(models.Model):

    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    bloodgroup = models.CharField(max_length=5)
    phone = models.CharField(max_length=20)
