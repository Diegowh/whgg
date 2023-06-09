from django.db import models

class SummonerModel(models.Model):
    summoner_puuid = models.CharField(max_length=200, primary_key=True, unique=True)
    summoner_id = models.CharField(max_length=200)
    summoner_name = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    last_update = models.DateTimeField(null=True)
    soloq_rank = models.CharField(max_length=200, default='Unranked')
    soloq_lp = models.IntegerField(default=0)
    soloq_wins = models.IntegerField(default=0)
    soloq_losses = models.IntegerField(default=0)
    soloq_wr = models.IntegerField(default=0)
    flex_rank = models.CharField(max_length=200, default='Unranked')
    flex_lp = models.IntegerField(default=0)
    flex_wins = models.IntegerField(default=0)
    flex_losses = models.IntegerField(default=0)
    flex_wr = models.IntegerField(default=0)
    profile_icon_id = models.IntegerField(null=True)
    summoner_level = models.IntegerField(null=True)


class ChampionStatsModel(models.Model):
    summoner = models.ForeignKey(SummonerModel, on_delete=models.CASCADE, related_name='champion_stats')
    champion_name = models.CharField(max_length=200)
    matches_played = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    wr = models.FloatField()
    kda = models.FloatField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    cs = models.IntegerField()


class MatchModel(models.Model):
    summoner = models.ForeignKey(SummonerModel, on_delete=models.CASCADE, related_name='matches')
    match_id = models.CharField(max_length=200)
    champion_name = models.CharField(max_length=200)
    win = models.IntegerField()
    kills = models.FloatField()
    deaths = models.FloatField()
    assists = models.FloatField()
    kda = models.FloatField()
    cs = models.IntegerField()
    vision = models.IntegerField()
    summoner_spell1 = models.IntegerField()
    summoner_spell2 = models.IntegerField()
    item0 = models.IntegerField()
    item1 = models.IntegerField()
    item2 = models.IntegerField()
    item3 = models.IntegerField()
    item4 = models.IntegerField()
    item5 = models.IntegerField()
    item6 = models.IntegerField()
    participant_summoner_names = models.JSONField()
    participant_champion_names = models.JSONField()
    participant_team_ids = models.JSONField()
    game_mode = models.CharField(max_length=200)
    game_duration = models.IntegerField()
    queue_id = models.IntegerField()
    team_position = models.CharField(max_length=200)