from django.db import models

class ChampionStats(models.Model):
    name = models.CharField(max_length=200)
    games = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    winrate = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    kda = models.FloatField()
    minion_kills = models.IntegerField()
    
    # Foreign Keys
    summoner = models.ForeignKey('Summoner', on_delete=models.CASCADE, related_name='champion_stats')
    
    class Meta:
        unique_together = ("name", "summoner")