from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.views import generic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from rest_framework import filters, viewsets
from rest_framework import permissions
from django.core import serializers
from .serializer import RaritySerializer, ItemSerializer, GameSerializer
from .models import Game, Rarity, Item
import random

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rarity_id', 'id']
    filterset_fields = ['rarity_id']

    def list(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        if id is not None:
            obj = get_object_or_404(self.queryset, id=id)
            serializer = self.get_serializer(obj)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)

class RarityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rarities to be viewed or edited.
    """
    queryset = Rarity.objects.all()
    serializer_class = RaritySerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['game_id', 'id']
    filterset_fields = ['game_id']

    def list(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        if id is not None:
            obj = get_object_or_404(self.queryset, id=id)
            serializer = self.get_serializer(obj)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)
    

class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']
    
    def list(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        if id is not None:
            obj = get_object_or_404(self.queryset, id=id)
            serializer = self.get_serializer(obj)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)
    

class Gacha(APIView):
    populated = False
    pity = dict()
    choices = []
    weights = []
    currpity = dict()
    raritylookup = dict()
    softpity = dict()
    softpitychance = dict()
    itemLookup = dict()
    itemChanceLookup = dict()

    def populate(self, game_id):
        game = get_object_or_404(Game, pk=game_id)
        rarities = game.rarity_set.all()
        for rarity in rarities:
            self.raritylookup[rarity.id] = rarity
            self.choices.append(rarity.id)
            self.weights.append(rarity.chance)
            if rarity.pity != 0:
                self.pity[rarity.id] = rarity.pity
                if rarity.softpity != 0:
                    self.softpity[rarity.id] = rarity.softpity
                    self.softpitychance[rarity.id] = rarity.softpitychance
            items = rarity.item_set.all()
            self.itemChanceLookup[rarity.id] = {"itemname": [], "chance": []}
            for item in items:
                self.itemLookup[item.item_name] = item
                self.itemChanceLookup[rarity.id]["itemname"].append(item.item_name)
                self.itemChanceLookup[rarity.id]["chance"].append(item.chance)
        self.currpity = self.pity.copy()
        for key in self.currpity:
            self.currpity[key] = 0
        self.populated = True

    # give us an updated pity, return what roll we got
    def roll(self): 
        atPity = None
        # check pity
        for key in self.currpity:
            if self.currpity[key] == self.pity[key] - 1:
                atPity = key
                break
        
        # check if we are at pity
        if atPity:
            self.tickPity()
            self.currpity[key] = 0
            return atPity
    
        atSoftPity = None
        for key in self.softpity:
            if self.currpity[key] >= self.softpity[key]:
                atSoftPity = key
                break
        
        # check if we are at pity
        if atSoftPity:
            self.tickPity()
            firstroll = random.random()
            if firstroll < self.softpitychance[atSoftPity]:
                self.currpity[atSoftPity] = 0
                return atSoftPity
            position = self.choices.index(atSoftPity)
            tempchoices, tempweights = self.choices.copy(), self.weights.copy()
            del tempchoices[position]
            del tempweights[position]
            roll = random.choices(tempchoices, tempweights)[0]
            if roll in self.currpity:
                self.currpity[roll] = 0
            return roll

        # we are not at pity, do a random roll
        roll = random.choices(self.choices, self.weights)[0]
        # check if roll is one with pity
        self.tickPity()
        if roll in self.currpity:
            self.currpity[roll] = 0
        return roll
        
    def tickPity(self):
        for key in self.currpity:
            self.currpity[key] += 1

    def get_item(self, rarity):
        item_names, item_chances = self.itemChanceLookup[rarity]["itemname"], self.itemChanceLookup[rarity]["chance"]
        roll = random.choices(item_names, item_chances)[0]
        return self.itemLookup[roll]
    
    def get(self, request, game_id):
        if not self.populated:
            self.populate(game_id)
        numrolls = int(request.GET.get('numrolls', ''))
        res = []
        for i in range(numrolls):
            rarity = self.roll()
            roll = RaritySerializer(self.raritylookup[rarity]).data
            item = ItemSerializer(self.get_item(rarity)).data
            print(self.currpity)
            res.append({"rarity": roll, "item": item, "pity": self.currpity.copy()})
        
        return Response(res)
    