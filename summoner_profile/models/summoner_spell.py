from django.db import models

class SummonerSpell(models.Model):
    id = models.IntegerField(max_length=200, primary_key=True, unique=True)
    name = models.CharField(max_length=200)