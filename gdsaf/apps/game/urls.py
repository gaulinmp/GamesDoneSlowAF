from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    path('', views.GameIndexView.as_view(), name='index'),
    path('overwatch', views.OverwatchView.as_view(), name='overwatch'),
    path('overwatch_upload', login_required(TemplateView.as_view(template_name='game/overwatch/form.html')), name='overwatch_upload'),
]

app_name = 'game'
