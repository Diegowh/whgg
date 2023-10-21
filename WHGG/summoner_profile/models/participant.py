from django.db import models

class Participant(models.Model):
    id = models.CharField(max_length=200, primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    champion_name = models.CharField(max_length=200)
    team_id = models.IntegerField()
    
    summoner_match = models.ForeignKey('SummonerMatch', on_delete=models.CASCADE, related_name='participants')