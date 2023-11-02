from django.db import models


class Version(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(unique=True, max_length=50)