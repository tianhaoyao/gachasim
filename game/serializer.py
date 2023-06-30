from rest_framework import serializers
from .models import Rate, Item, Game

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'game', 'rarity', 'chance', 'pity', 'softpity', 'softpitychance', 'color']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'rate', 'item_name', 'image', 'chance']
    
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", 'game_name', "image"]
