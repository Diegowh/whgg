# Generated by Django 4.2.6 on 2023-12-04 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summoner_profile', '0003_alter_match_game_duration_alter_match_game_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championstats',
            name='assists',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='deaths',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='championstats',
            name='kills',
            field=models.FloatField(),
        ),
    ]