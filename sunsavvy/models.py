from django.db import models

# Create your models here.

class API_data(models.Model):
    #Hourly data
    date = [models.CharField(max_length=200, null=True)] * 24
    UV = [models.FloatField()]*24
