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
from .serializer import RateSerializer, ItemSerializer, GameSerializer
from .models import Game, Rate, Item
import random

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    queryset = Item.objects.all().order_by('rate')
    serializer_class = ItemSerializer


class RateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rates to be viewed or edited.
    """
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    def get_queryset(self):
        queryset = self.queryset
        game = self.request.query_params.get('game')
        if not game:
            return queryset
        query_set = queryset.filter(game=game)
        return query_set
    

class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rates to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    

class Gacha(APIView):
    populated = False
    pity = dict()
    choices = []
    weights = []
    currpity = dict()
    ratelookup = dict()
    softpity = dict()
    softpitychance = dict()
    itemLookup = dict()
    itemChanceLookup = dict()

    def populate(self, game_id):
        game = get_object_or_404(Game, pk=game_id)
        rates = game.rate_set.all()
        for rate in rates:
            self.ratelookup[rate.rarity] = rate
            self.choices.append(rate.rarity)
            self.weights.append(rate.chance)
            if rate.pity != 0:
                self.pity[rate.rarity] = rate.pity
                if rate.softpity != 0:
                    self.softpity[rate.rarity] = rate.softpity
                    self.softpitychance[rate.rarity] = rate.softpitychance
            items = rate.item_set.all()
            self.itemChanceLookup[rate.rarity] = {"itemname": [], "chance": []}
            for item in items:
                self.itemLookup[item.item_name] = item
                self.itemChanceLookup[rate.rarity]["itemname"].append(item.item_name)
                self.itemChanceLookup[rate.rarity]["chance"].append(item.chance)
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

    def get_item(self, rate):
        item_names, item_chances = self.itemChanceLookup[rate]["itemname"], self.itemChanceLookup[rate]["chance"]
        roll = random.choices(item_names, item_chances)[0]
        return self.itemLookup[roll]
    
    def get(self, request, game_id):
        if not self.populated:
            self.populate(game_id)
        numrolls = int(request.GET.get('numrolls', ''))
        res = []
        for i in range(numrolls):
            rate = self.roll()
            roll = RateSerializer(self.ratelookup[rate]).data
            item = ItemSerializer(self.get_item(rate)).data
            print(self.currpity)
            res.append({"rate": roll, "item": item, "pity": self.currpity.copy()})
        
        return Response(res)

class GameView(APIView):
    def get(self, request, game_id):
        game = GameSerializer(get_object_or_404(Game, pk=game_id)).data
        return Response(game)