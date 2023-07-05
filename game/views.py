from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
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

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

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

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

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

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        if id is not None:
            obj = get_object_or_404(self.queryset, id=id)
            serializer = self.get_serializer(obj)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)


class Gacha(APIView):
    populated = False
    game_id = -1
    pity = dict()
    choices = []
    weights = []
    currpity = dict()
    rarityByIdHash = dict()
    softpity = dict()
    softpitychance = dict()
    itemLookup = dict()
    itemChanceLookup = dict()
    permission_classes = [AllowAny]

    def reset(self):
        self.populated = False
        self.pity = dict()
        self.choices = []
        self.weights = []
        self.currpity = dict()
        self.rarityByIdHash = dict()
        self.softpity = dict()
        self.softpitychance = dict()
        self.itemLookup = dict()
        self.itemChanceLookup = dict()

    def populate(self, game_id):
        game = get_object_or_404(Game, pk=game_id)
        if game_id != self.game_id:
            self.reset()
            self.game_id = game_id
        rarities = game.rarity_set.all()

        for rarity in rarities:
            self.rarityByIdHash[rarity.id] = rarity
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
                self.itemChanceLookup[rarity.id]["itemname"].append(
                    item.item_name)
                self.itemChanceLookup[rarity.id]["chance"].append(item.chance)
        self.currpity = self.pity.copy()
        for key in self.currpity:
            self.currpity[key] = 0
        self.populated = False

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
        item_names, item_chances = self.itemChanceLookup[rarity][
            "itemname"], self.itemChanceLookup[rarity]["chance"]
        roll = random.choices(item_names, item_chances)[0]
        return self.itemLookup[roll]

    def get(self, request, game_id):
        if not self.populated:
            self.populate(game_id)
        # if one of the data structures not populated, cannot roll.
        if not self.rarityByIdHash or not self.itemLookup:
            return Response([])
        numrolls = int(request.GET.get('numrolls', ''))
        res = []
        for i in range(numrolls):
            rarity_id = self.roll()
            rarity = RaritySerializer(self.rarityByIdHash[rarity_id]).data
            item = ItemSerializer(self.get_item(rarity_id)).data
            res.append({"rarity": rarity, "item": item,
                       "pity": self.currpity.copy()})

        return Response(res)
