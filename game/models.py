from django.db import models
import datetime
from django.utils import timezone
from colorfield.fields import ColorField
    
class Game(models.Model):
    game_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to ='game/uploads/')

    def __str__(self):
        return self.game_name

class Rate(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rarity = models.IntegerField(default=0)
    chance = models.FloatField(default=0)
    pity = models.IntegerField(default=0)
    softpity = models.IntegerField(default=0)
    softpitychance = models.FloatField(default=0)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return str(self.game.game_name + str(self.rarity))

class Item(models.Model):
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to ='game/uploads/')
    chance = models.FloatField(default=0)
    
    def __str__(self):
        return self.item_name