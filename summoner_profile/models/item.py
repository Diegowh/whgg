from django.db import models

class Item(models.Model):
    id = models.IntegerField(max_length=200, primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    explanation = models.CharField(max_length=200, null=True)
    description = models.TextField()
    base_gold = models.IntegerField()
    total_gold = models.IntegerField()