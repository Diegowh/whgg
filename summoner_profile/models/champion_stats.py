from django.db import models


class ChampionStats(models.Model):
    name = models.CharField(max_length=200)
    games = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    winrate = models.IntegerField(default=0)
    kills = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    deaths = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    assists = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    kda = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    minion_kills = models.DecimalField(
        max_digits=5, decimal_places=1, default=0.0)

    # Foreign Keys
    summoner = models.ForeignKey(
        'Summoner', on_delete=models.CASCADE, related_name='champion_stats')

    class Meta:
        unique_together = ("name", "summoner")
