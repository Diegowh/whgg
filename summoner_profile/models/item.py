from django.db import models

class Item(models.Model):
    id = models.IntegerField(max_length=200, primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    plaintext = models.CharField(max_length=200, null=True)
    description = models.TextField()
    gold_base = models.IntegerField()
    gold_total = models.IntegerField()