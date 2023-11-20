from django.db import models

class Match(models.Model):
    id = models.CharField(max_length=200, primary_key=True, unique=True)
    game_start = models.IntegerField()
    game_end = models.IntegerField()
    game_duration = models.IntegerField()
    game_mode = models.CharField()
    game_type = models.CharField()
    champion_played = models.CharField(max_length=200)
    win = models.BooleanField()
    kills = models.IntegerField()   
    deaths = models.IntegerField()
    assists = models.IntegerField()
    kda = models.FloatField()
    minion_kills = models.IntegerField()
    vision_score = models.IntegerField()
    team_position = models.CharField(max_length=200)
    team_id = models.IntegerField()
    
    # Foreign Keys
    summoner = models.ForeignKey('Summoner', on_delete=models.CASCADE, related_name='summoner_matches')

    item_purchase = models.ManyToManyField('Item', related_name='summoner_matches')
    
    summoner_spells = models.ManyToManyField('SummonerSpell', related_name='summoner_matches')
    
    # Puedo acceder a todos los participantes de un Match a traves de match.participants.all()