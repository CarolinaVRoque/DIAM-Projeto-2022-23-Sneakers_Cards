from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'SneakerCards'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('add_card', views.add_cards, name='add_cards'),
    path('view_cards', views.view_cards, name='view_cards'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('my_deck', views.my_deck, name='my_deck'),
    path('buy_booster', views.buy_booster, name='buy_booster'),
    path('update_deck', views.update_deck, name='update_deck'),
    path('view_deck/<int:collector_id>/<int:deck_id>', views.view_deck, name='view_deck'),
    path('sell_card/<int:card_id>/<int:deck_id>/', views.sell_card, name='sell_card'),
    path('openBooster', views.openBooster, name='openBooster'),
    path('trade_for_credits/<int:card_id>/', views.trade_for_credits, name='trade_for_credits'),
    path('add_card_deck/<int:card_id>/<int:deck_id>/', views.add_card_deck, name='add_card_deck'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
