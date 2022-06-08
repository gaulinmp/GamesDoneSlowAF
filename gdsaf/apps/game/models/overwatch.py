# STDlib imports

# 3rd party imports
from django.db import models as djm
# from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
# from django.conf import settings
# replace user below with settings.AUTH_USER_MODEL if overriding User

# current module imports

POINTS_PER_DAMAGE = 1
POINTS_PER_BLOCK = 1
POINTS_PER_HEAL = 1.1
POINTS_PER_KILL = 500
POINTS_PER_ASSIST = 500
POINTS_PER_DEATH = -500
POINTS_PER_OBJECTIVE_SECOND = 10
POINTS_PER_POTG = 1000
POINTS_PER_CARD = 500
POINTS_PER_FRIEND = 500
LOSS_SCALAR = .72

class OverwatchManager(djm.Manager):
    def get_queryset(self):
        """Overrides the djm.Manager method"""
        return (
            super()
            .get_queryset()
            .annotate(total_points = djm.ExpressionWrapper(
                    ( djm.F('num_damage') * djm.Value(POINTS_PER_DAMAGE)
                    + djm.F('num_blocked') * djm.Value(POINTS_PER_BLOCK)
                    + djm.F('num_healed') * djm.Value(POINTS_PER_HEAL)
                    + djm.F('num_kills') * djm.Value(POINTS_PER_KILL)
                    + djm.F('num_assists') * djm.Value(POINTS_PER_ASSIST)
                    + djm.F('num_deaths') * djm.Value(POINTS_PER_DEATH)
                    + djm.F('objective_time') * djm.Value(POINTS_PER_OBJECTIVE_SECOND)
                    + djm.F('got_potg') * djm.Value(POINTS_PER_POTG)
                    + djm.F('got_card') * djm.Value(POINTS_PER_CARD)
                    + djm.F('with_friend') * djm.Value(POINTS_PER_FRIEND)
                    ) * (djm.F('did_win') * djm.Value(1-LOSS_SCALAR) + djm.Value(LOSS_SCALAR)),
                output_field=djm.IntegerField())
            ) # end annotate
        ) # end return

class Overwatch(djm.Model):
    user = djm.ForeignKey(User, on_delete=djm.CASCADE)
    datetime = djm.DateTimeField(auto_now_add=True)

    # Base points - best of either damage dealt, healing, damage blocked
    num_damage = djm.IntegerField("Damage Dealt", default=0)
    num_blocked = djm.IntegerField("Damage Blocked", default=0)
    num_healed = djm.IntegerField("Healing Done", default=0)
    # +500 pts for each kill / kill assist (not sure what relevant stats are for healers)
    num_kills = djm.IntegerField("Number of Kills", default=0)
    num_assists = djm.IntegerField("Number of Assists", default=0)
    # -500 pts for each death
    num_deaths = djm.IntegerField("Number of Deaths", default=0)
    # +any objective time x10 (in seconds)
    objective_time = djm.IntegerField("Objective Time (seconds)", default=0)
    # +1000 pts for potg
    got_potg = djm.BooleanField("Got POTG?", default=False)
    # +500 pts for any card
    got_card = djm.BooleanField("Got a Card?", default=False)
    # total x1.25 for a win; x0.9 for a loss ~= to 1 for win, .72 for loss
    did_win = djm.BooleanField("Did you win?", default=False)
    # +500 pts for playing with friend
    with_friend = djm.BooleanField("Played with friend?", default=False)

    # manager
    objects = OverwatchManager()

    # for forms
    bool_fields = ['got_potg', 'got_card', 'did_win', 'with_friend']
    upload_fields = ['num_damage', 'num_blocked', 'num_healed', 'num_kills', 'num_assists', 'num_deaths',
                     'objective_time', *bool_fields]

    def __str__(self):
        try:
            return f"{self.user} @ {self.datetime:%b-%d %H:%M} == {self.total_points:,.0f}"
        except AttributeError:
            pass
        return f"{self.user} @ {self.datetime:%b-%d %H:%M}"
