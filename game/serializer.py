from rest_framework import serializers
from .models import Rarity, Item, Game

class RaritySerializer(serializers.ModelSerializer):
    game_id = serializers.PrimaryKeyRelatedField(source='game', queryset=Game.objects.all())
    class Meta:
        model = Rarity
        fields = ['id', 'game_id', 'rarity_name', 'chance', 'pity', 'softpity', 'softpitychance', 'color']

class ItemSerializer(serializers.ModelSerializer):
    rarity_id = serializers.PrimaryKeyRelatedField(source='rarity', queryset=Rarity.objects.all())
    class Meta:
        model = Item
        fields = ['id', 'rarity_id', 'item_name', 'image', 'chance']
    
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", 'game_name', "image"]
