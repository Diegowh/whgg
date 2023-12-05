from django.db import models

class Item(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    plaintext = models.TextField(null=True)
    description = models.TextField()
    gold_base = models.IntegerField()
    gold_total = models.IntegerField()