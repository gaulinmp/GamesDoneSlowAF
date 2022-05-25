# STDlib imports

# 3rd party imports
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

# current module imports


class Overwatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    # Base points - best of either damage dealt, healing, damage blocked
    num_damage = models.IntegerField("Damage Dealt", default=0)
    num_blocked = models.IntegerField("Damage Blocked", default=0)
    num_healed = models.IntegerField("Healing Done", default=0)
    POINTS_PER_HEAL = 1.1
    # +500 pts for each kill / kill assist (not sure what relevant stats are for healers)
    num_kills = models.IntegerField("Number of Kills", default=0)
    POINTS_PER_KILL = 500
    num_assists = models.IntegerField("Number of Assists", default=0)
    POINTS_PER_ASSIST = 500
    # -500 pts for each death
    num_deaths = models.IntegerField("Number of Deaths", default=0)
    POINTS_PER_DEATH = -500
    # +any objective time x10 (in seconds)
    objective_time = models.IntegerField("Objective Time (seconds)", default=0)
    POINTS_PER_OBJECTIVE_SECOND = 10
    # +1000 pts for potg
    got_potg = models.BooleanField("Got POTG?", default=False)
    POINTS_PER_POTG = 1000
    # +500 pts for any card
    got_card = models.BooleanField("Got a Card?", default=False)
    POINTS_PER_CARD = 500
    # total x1.25 for a win; x0.9 for a loss ~= to 1 for win, .72 for loss
    did_win = models.BooleanField("Did you win?")
    LOSS_SCALAR = .72

    def get_points(self):
        return (
            self.num_damage
            + self.num_blocked
            + self.num_healed * self.POINTS_PER_HEAL
            + self.num_kills * self.POINTS_PER_KILL
            + self.num_assists * self.POINTS_PER_ASSIST
            + self.num_deaths * self.POINTS_PER_DEATH
            + self.objective_time * self.POINTS_PER_OBJECTIVE_SECOND
            + self.got_potg * self.POINTS_PER_POTG
            + self.got_card * self.POINTS_PER_CARD
        ) * (int(self.did_win) * (1-self.LOSS_SCALAR) + self.LOSS_SCALAR)

    def __str__(self):
        return f"{self.user} @ {self.datetime:%b-%d %H:%M} == {self.get_points():,.0f}"
