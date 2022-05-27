
# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render, redirect

from .models import Overwatch

def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    data = {"games": "Overwatch"}

    return render(request, 'game/index.html', data)


@login_required
def overwatch(request):
    keep_fields = 'id username first_name last_name'.split()

    user_agg = (
        Overwatch.objects
        .values('user')
        .order_by('user')
        .annotate(overall_total=models.Sum('total_points'))
    )
    agg_stats = {}
    for u in user_agg:
        agg_stats[u['user']] = {'overall_total': u['overall_total']}

    for usr in User.objects.filter(id__in=agg_stats.keys()).values():
        if usr['id'] not in agg_stats: continue
        _d = agg_stats[usr['id']]
        for c in keep_fields:
            _d[c] = usr[c]

    data = {
        'all_ow_games': Overwatch.objects.all(),
        'ow_agg': sorted(agg_stats.values(), key=lambda x: x['overall_total'], reverse=True),
    }

    return render(request, 'game/overwatch.html', data)
