from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('overwatch', views.overwatch, name='overwatch'),
]

app_name = 'game'
