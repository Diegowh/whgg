from django.db import models


class Season(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(unique=True)