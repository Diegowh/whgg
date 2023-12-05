import time
from django.db import models

class Version(models.Model):
    version = models.CharField(max_length=200, primary_key=True, unique=True, default='0.0.0')
    
    def __str__(self):
        return self.version
