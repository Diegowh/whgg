from django.db import models

class SummonerSpell(models.Model):
    id = models.CharField(max_length=200,primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    key = models.IntegerField(default=0)
    description = models.TextField(max_length=300)
    image_name = models.CharField(max_length=200)
    sprite_name = models.CharField(max_length=200)