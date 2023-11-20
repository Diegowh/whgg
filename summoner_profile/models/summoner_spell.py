from django.db import models

class SummonerSpell(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    image_name = models.CharField(max_length=200)
    sprite_name = models.CharField(max_length=200)