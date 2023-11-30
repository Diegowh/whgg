from django.db import models

class Summoner(models.Model):
    puuid = models.CharField(max_length=200, primary_key=True, unique=True)
    id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    icon_id = models.IntegerField()
    summoner_level = models.IntegerField()
    last_update = models.BigIntegerField()