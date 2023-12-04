from django.db import models

class ChampionStats(models.Model):
    name = models.CharField(max_length=200)
    games = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    winrate = models.IntegerField()
    kills = models.DecimalField(max_digits= 5, decimal_places=1)
    deaths = models.DecimalField(max_digits= 5, decimal_places=1)
    assists = models.DecimalField(max_digits= 5, decimal_places=1)
    kda = models.DecimalField(max_digits=5, decimal_places=2)
    minion_kills = models.DecimalField(max_digits=5, decimal_places=1)
    
    # Foreign Keys
    summoner = models.ForeignKey('Summoner', on_delete=models.CASCADE, related_name='champion_stats')
    
    class Meta:
        unique_together = ("name", "summoner")