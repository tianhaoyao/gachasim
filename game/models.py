from django.db import models
import datetime
from django.utils import timezone
from colorfield.fields import ColorField
from django.contrib.auth.models import User
    
class Game(models.Model):
    game_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to ='game/uploads/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.game_name

class Rarity(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rarity_name = models.CharField(max_length=200)
    chance = models.FloatField(default=0)
    pity = models.IntegerField(default=0)
    softpity = models.IntegerField(default=0)
    softpitychance = models.FloatField(default=0)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return "{}-{}".format(self.game.game_name, str(self.rarity_name))
    
class Item(models.Model):
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to ='game/uploads/')
    chance = models.FloatField(default=0)
    
    def __str__(self):
        return self.item_name