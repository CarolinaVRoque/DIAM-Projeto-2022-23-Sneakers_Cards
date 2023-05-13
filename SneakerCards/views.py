from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from SneakerCards.models import Collector, CardType, Cards, Deck
from django.core import serializers
from django.core.cache import cache
import random


# Create your views here.
def index(request):
    return render(request, 'SneakerCards/index.html')


def about(request):
    return render(request, 'SneakerCards/about.html')


def register(request):
    if request.method == 'POST':
        password = request.POST['password']
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        user = User.objects.create_user(username, email, password)
        collector = Collector.objects.create(user=user, full_name=full_name, nickname=username, power=0)
        collector.save()
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            fs = FileSystemStorage()
            filename = fs.save(avatar.name, avatar)
            uploaded_file_url = fs.url(filename)
            # had to remove first '/' because of linux
            collector.avatar = uploaded_file_url[1:]
            collector.save()
        else:
            default_image = 'SneakerCards/images/person_empty_holder.png'
            fs = FileSystemStorage()
            uploaded_file_url = fs.url(default_image)
            collector.avatar = uploaded_file_url[1:]
            collector.save()
        if collector.pk is not None:
            return HttpResponseRedirect(reverse('SneakerCards:index'))
    else:
        return render(request, 'SneakerCards/register.html')


def login(request):
    if request.method == 'POST':
        try:
            password = request.POST['password']
            username = request.POST['username']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                request.session['username'] = user.username
                return render(request, 'SneakerCards/index.html')
            else:
                error_message = "Username or password incorrect"
                return render(request, 'SneakerCards/login.html', {'error_message': error_message})
        except KeyError:
            error_message = "Error logging in"
            return render(request, 'SneakerCards/login.html', {'error_message': error_message})
    else:
        return render(request, 'SneakerCards/login.html')


def add_cards(request):
    card_types = CardType.objects.all()
    if request.method == 'POST':
        try:
            cardname = request.POST['card_name']
            cardtypeid = request.POST['card_type']
            carddesc = request.POST['card_descript']
            cardtype = CardType.objects.get(id=cardtypeid)

            if 'card_pic' in request.FILES:
                cardpic = request.FILES['card_pic']
                fs = FileSystemStorage()
                filename = fs.save(cardpic.name, cardpic)
                uploaded_file_url = fs.url(filename)
                # had to remove first '/' because of linux
                cardpic = uploaded_file_url[1:]
            else:
                error_message = "Missing card pic"
                return render(request, 'SneakerCards/add_cards.html', {'error_message': error_message})

            card = Cards.objects.create(name=cardname, card_type=cardtype, image=cardpic, description=carddesc)
            card.save()
            sucess_message = "Card added successfully"

            return render(request, 'SneakerCards/add_cards.html', {'sucess_message': sucess_message,
                                                                   'card_types': card_types})
        except KeyError:
            error_message = "Error adding card exception"
            return render(request, 'SneakerCards/add_cards.html', {'error_message': error_message})
    else:
        return render(request, 'SneakerCards/add_cards.html', {'card_types': card_types})


def view_cards(request):
    cards = Cards.objects.all()
    print(cards)
    return render(request, 'SneakerCards/view_cards.html', {'cards': cards})


def buy_booster(request):
    userid = request.session.get('username')
    user_info = User.objects.get(username=userid)
    return render(request, 'SneakerCards/buy_booster.html', {'userInfo': user_info})


def dashboard(request):
    userid = request.session.get('username')
    user_info = User.objects.get(username=userid)
    return render(request, 'SneakerCards/dashboard.html', {'userInfo': user_info})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('SneakerCards:index'))


def my_deck(request):
    collector = get_object_or_404(Collector, user=request.user)
    decks = Deck.objects.filter(collector=collector)
    return render(request, 'SneakerCards/my_decks.html', {'decks': decks})


def update_deck(request):
    collector = get_object_or_404(Collector, user=request.user)
    decks = Deck.objects.filter(collector=collector)
    print("Form submitted successfully")
    if request.method == 'POST':
        deck_name = request.POST.get('deck_name')
        print(deck_name)
        deck = Deck.objects.create(name=deck_name, power=30, collector=collector)
        deck.save()
        return redirect('SneakerCards:my_deck')
    return render(request, 'SneakerCards/my_decks.html', {'decks': decks})


def view_deck(request, collector_id, deck_id):
    collector = get_object_or_404(Collector, pk=collector_id)
    deck = get_object_or_404(Deck, pk=deck_id, collector=collector)
    cards = deck.cards.all()
    if len(cards) == 0:
        print("null")
        return render(request, 'SneakerCards/view_deck_cards.html', {'deck': deck})
    else:
        print(cards)
        return render(request, 'SneakerCards/view_deck_cards.html', {'cards': cards, 'deck': deck})


def sell_card(request, card_id, deck_id):
    throught_model = Deck.cards.through
    assc_id = throught_model.objects.filter(cards__id=card_id, deck__id=deck_id).values_list('id', flat=True).first()
    print(card_id)
    throught_model.objects.filter(id=assc_id).delete()
    collector = Collector.objects.get(pk=request.user.id)
    price = Cards.objects.get(pk=card_id).card_type.saleValue
    collector.credits += price
    collector.save()
    return redirect('SneakerCards:view_deck', collector_id=request.user.id, deck_id=deck_id)


def openBooster(request):
    collector = get_object_or_404(Collector, user=request.user)
    decks = decks = Deck.objects.filter(collector=collector)
    source = request.GET.get('source')
    cards = []
    multiplier = 1

    if source == 'prince':
        multiplier = 1
        collector.credits -= 100
    elif source == 'monarch':
        multiplier = 2
        collector.credits -= 175
    elif source == 'king':
        multiplier = 3
        collector.credits -= 250
    else:
        return render(request, 'SneakerCards/buy_booster.html', {'error_message': 'Error. Invalid source'})

    if collector.credits < 0:
        user_info = User.objects.get(username=request.session.get('username'))
        return render(request, 'SneakerCards/buy_booster.html', {'error_message': 'Insuficient credits',
                                                                 'userInfo': user_info})

    collector.save()
    card_types = CardType.objects.all()
    cardtype_probabilities = {}
    total_probability = 0
    for card_type in card_types:
        cardtype_probabilities[card_type.type] = card_type.percentage
        total_probability += card_type.percentage
    for card_type, probability in cardtype_probabilities.items():
        cardtype_probabilities[card_type] = probability / total_probability

    for i in range(0, 5):
        random_number = random.uniform(0, 1)
        cumalitve_probability = 0
        for card_type, probability in cardtype_probabilities.items():
            # Não sei se é assim que vou controlar os multiplicadores
            # preciso do Nuno!! xD
            cumalitve_probability += probability * multiplier
            if random_number < cumalitve_probability:
                selected_cardtype = card_type
                break
        random_card = Cards.objects.filter(card_type__type=selected_cardtype).order_by('?').first()
        cards.append(random_card)
    return render(request, 'SneakerCards/open_booster.html', {'cards': cards, 'decks': decks})


def trade_for_credits(request, card_id):
    card = Cards.objects.get(pk=card_id)
    collector = Collector.objects.get(pk=request.user.id)
    collector.credits += card.card_type.saleValue
    collector.save()
    return HttpResponse(status=200)


def add_card_deck(request, card_id, deck_id):
    if request.method == 'POST':
        print("post")
        card = Cards.objects.get(pk=card_id)
        collector = Collector.objects.get(pk=request.user.id)
        deck = get_object_or_404(Deck, pk=deck_id, collector=collector)
        deck.cards.add(card)
        deck.save()
        return HttpResponse(status=200)
    else:
        return render(request, 'SneakerCards/open_booster.html')
