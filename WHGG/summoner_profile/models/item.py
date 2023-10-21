from django.db import models

class Item(models.Model):
    id = models.CharField(max_length=200, primary_key=True, unique=True)
    name = models.CharField(max_length=200)