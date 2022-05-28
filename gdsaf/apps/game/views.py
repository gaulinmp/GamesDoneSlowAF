
# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView


from .models import Overwatch

KEEP_USER_FIELDS = ['id', 'username', 'first_name', 'last_name']

class GameIndexView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        user_with_agg = {u['id']:{**dict(u), 'total_points':0} for u in User.objects.all().values(*KEEP_USER_FIELDS)}

        for game in [OverwatchView]:
            for _id,_tot in game().aggregate_points().items():
                if _id in user_with_agg:
                    user_with_agg[_id]['total_points'] += _tot

        data = {
            'all_aggregate': sorted(user_with_agg.values(), key=lambda x: x['total_points'], reverse=True),
        }

        return render(request, 'game/index.html', data)


class GenericGameView(LoginRequiredMixin, CreateView):

    model = None
    template_dir = None

    def aggregate_points(self):
        user_agg = (
            self.model
            .objects
            .values('user')
            .order_by('user')
            .annotate(overall_total=models.Sum('total_points'))
        )

        return {u['user']: u['overall_total'] for u in user_agg}

    def get(self, request, *args, **kwargs):
        game_totals = self.aggregate_points()

        user_with_agg = [{**dict(u), 'total_points':game_totals[u['id']]}
                         for u in User.objects.filter(id__in=game_totals.keys()).values(*KEEP_USER_FIELDS)]

        data = {
            'all_games': self.model.objects.all(),
            'game_aggregate': sorted(user_with_agg, key=lambda x: x['total_points'], reverse=True),
        }

        return render(request, f"game/{self.template_dir}/get.html", data)

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     # print(request.POST['num_damage'])

    #     return self.get(request, *args, **kwargs)

class OverwatchView(GenericGameView):
    model = Overwatch
    template_dir = "overwatch"
    template_name = "game/overwatch/get.html"
    fields = Overwatch.upload_fields
    success_url = reverse_lazy('game:overwatch')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        newpost = request.POST.copy()
        for _field in Overwatch.bool_fields:
            if _field in newpost:
                newpost[_field] = True
            else:
                newpost[_field] = False
        request.POST = newpost
        print(request.POST)
        # print(request.POST['num_damage'])

        return super().post(request, *args, **kwargs)
