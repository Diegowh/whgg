from django.db import models

class SummonerMatch(models.Model):
    id = models.IntegerField(max_length=200, primary_key=True, unique=True)
    