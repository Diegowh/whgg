from django.db import models

class SummonerMatch(models.Model):
    id = models.CharField(max_length=200, primary_key=True, unique=True)
    season_id = models.IntegerField() # https://static.developer.riotgames.com/docs/lol/seasons.json
    queue_id = models.IntegerField() # https://static.developer.riotgames.com/docs/lol/queues.json
    game_mode = models.CharField() # https://static.developer.riotgames.com/docs/lol/gameModes.json
    game_type = models.CharField() # https://static.developer.riotgames.com/docs/lol/gameTypes.json
    champion_name = models.CharField(max_length=200)
    win = models.BooleanField()
    kills = models.IntegerField()   
    deaths = models.IntegerField()
    assists = models.IntegerField()
    kda = models.FloatField()
    minion_kills = models.IntegerField()
    vision_score = models.IntegerField()
    team_position = models.CharField(max_length=200)
    
    # Foreign Keys
    summoner = models.ForeignKey('Summoner', on_delete=models.CASCADE, related_name='summoner_matches')

    item_purchase = models.ManyToManyField('Item', related_name='summoner_matches')
    
    summoner_spells = models.ManyToManyField('SummonerSpell', related_name='summoner_matches')