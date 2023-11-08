from django.db import models

class RankedStats(models.Model):
    id = models.CharField(max_length=200, primary_key=True, unique=True)
    queue_type = models.CharField(max_length=200)
    rank = models.CharField(max_length=200)
    league_points = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    winrate = models.IntegerField() # Lo quiero redondeado a un entero
    
    # Foreign Keys
    summoner = models.ForeignKey('Summoner', on_delete=models.CASCADE, related_name='ranked_stats')
    
    class Meta:
        unique_together = ("queue_type", "summoner")