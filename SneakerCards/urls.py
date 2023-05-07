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



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
