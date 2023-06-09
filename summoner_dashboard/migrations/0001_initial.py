# Generated by Django 4.2.1 on 2023-05-28 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SummonerModel',
            fields=[
                ('summoner_puuid', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('summoner_id', models.CharField(max_length=200)),
                ('summoner_name', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=200)),
                ('last_update', models.DateTimeField()),
                ('soloq_rank', models.CharField(default='Unranked', max_length=200)),
                ('soloq_lp', models.IntegerField(default=0)),
                ('soloq_wins', models.IntegerField(default=0)),
                ('soloq_losses', models.IntegerField(default=0)),
                ('soloq_wr', models.IntegerField(default=0)),
                ('flex_rank', models.CharField(default='Unranked', max_length=200)),
                ('flex_lp', models.IntegerField(default=0)),
                ('flex_wins', models.IntegerField(default=0)),
                ('flex_losses', models.IntegerField(default=0)),
                ('flex_wr', models.IntegerField(default=0)),
                ('profile_icon_id', models.IntegerField()),
                ('summoner_level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MatchModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.CharField(max_length=200)),
                ('champion_name', models.CharField(max_length=200)),
                ('win', models.IntegerField()),
                ('kills', models.FloatField()),
                ('deaths', models.FloatField()),
                ('assists', models.FloatField()),
                ('kda', models.FloatField()),
                ('cs', models.IntegerField()),
                ('vision', models.IntegerField()),
                ('summoner_spell1', models.IntegerField()),
                ('summoner_spell2', models.IntegerField()),
                ('item0', models.IntegerField()),
                ('item1', models.IntegerField()),
                ('item2', models.IntegerField()),
                ('item3', models.IntegerField()),
                ('item4', models.IntegerField()),
                ('item5', models.IntegerField()),
                ('item6', models.IntegerField()),
                ('participant_summoner_names', models.JSONField()),
                ('participant_champion_names', models.JSONField()),
                ('participant_team_ids', models.JSONField()),
                ('game_mode', models.CharField(max_length=200)),
                ('game_duration', models.IntegerField()),
                ('queue_id', models.IntegerField()),
                ('team_position', models.CharField(max_length=200)),
                ('summoner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='summoner_dashboard.summonermodel')),
            ],
        ),
        migrations.CreateModel(
            name='ChampionStatsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('champion_name', models.CharField(max_length=200)),
                ('matches_played', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('wr', models.FloatField()),
                ('kda', models.FloatField()),
                ('kills', models.IntegerField()),
                ('deaths', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('cs', models.IntegerField()),
                ('summoner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='champion_stats', to='summoner_dashboard.summonermodel')),
            ],
        ),
    ]
