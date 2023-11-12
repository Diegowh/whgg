# Generated by Django 4.2.6 on 2023-11-12 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.IntegerField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('plaintext', models.CharField(max_length=200, null=True)),
                ('description', models.TextField()),
                ('gold_base', models.IntegerField()),
                ('gold_total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('puuid', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('id', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('server', models.CharField(max_length=200)),
                ('icon_id', models.IntegerField()),
                ('summoner_level', models.IntegerField()),
                ('last_update', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SummonerSpell',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=300)),
                ('image_name', models.CharField(max_length=200)),
                ('sprite_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SummonerMatch',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('season_id', models.IntegerField()),
                ('queue_id', models.IntegerField()),
                ('game_mode', models.CharField()),
                ('game_type', models.CharField()),
                ('champion_name', models.CharField(max_length=200)),
                ('win', models.BooleanField()),
                ('kills', models.IntegerField()),
                ('deaths', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('kda', models.FloatField()),
                ('minion_kills', models.IntegerField()),
                ('vision_score', models.IntegerField()),
                ('team_position', models.CharField(max_length=200)),
                ('item_purchase', models.ManyToManyField(related_name='summoner_matches', to='summoner_profile.item')),
                ('summoner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='summoner_matches', to='summoner_profile.summoner')),
                ('summoner_spells', models.ManyToManyField(related_name='summoner_matches', to='summoner_profile.summonerspell')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('puuid', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('champion_name', models.CharField(max_length=200)),
                ('team_id', models.IntegerField()),
                ('summoner_match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='summoner_profile.summonermatch')),
            ],
        ),
        migrations.CreateModel(
            name='ChampionStats',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('games', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('winrate', models.IntegerField()),
                ('kills', models.IntegerField()),
                ('deaths', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('kda', models.FloatField()),
                ('minion_kills', models.IntegerField()),
                ('summoner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='champion_stats', to='summoner_profile.summoner')),
            ],
        ),
        migrations.CreateModel(
            name='RankedStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queue_type', models.CharField(max_length=200)),
                ('rank', models.CharField(max_length=200)),
                ('league_points', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('winrate', models.IntegerField()),
                ('summoner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ranked_stats', to='summoner_profile.summoner')),
            ],
            options={
                'unique_together': {('queue_type', 'summoner')},
            },
        ),
    ]
