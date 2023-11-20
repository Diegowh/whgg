from enum import unique
from django.db import models

class Participant(models.Model):
    puuid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    champion_name = models.CharField(max_length=200)
    team_id = models.IntegerField()
    
    match = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='participants')
    
    class Meta:
        unique_together = ("puuid", "match")