# Generated by Django 4.2.1 on 2023-05-28 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summoner_dashboard', '0002_alter_summonermodel_last_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summonermodel',
            name='profile_icon_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='summonermodel',
            name='summoner_level',
            field=models.IntegerField(null=True),
        ),
    ]
