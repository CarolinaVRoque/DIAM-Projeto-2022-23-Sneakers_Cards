from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Collector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    power = models.IntegerField()
    avatar = models.ImageField(upload_to='avatars', blank=True)
    deck = models.ForeignKey('Deck', on_delete=models.CASCADE, null=True)


class CardType(models.Model):
    descript = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    value = models.IntegerField()


class Cards(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=100)


class Deck(models.Model):
    cards = models.ManyToManyField(Cards)
    name = models.CharField(max_length=100)
    power = models.IntegerField(null=True)
