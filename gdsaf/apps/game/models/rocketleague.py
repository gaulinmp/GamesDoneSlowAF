# STDlib imports

# 3rd party imports
from django.db import models as djm

# from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

# from django.conf import settings
# replace user below with settings.AUTH_USER_MODEL if overriding User

# current module imports

POINTS_PER_POINT = 10
POINTS_PER_MVP = 500
LOSS_SCALAR = 0.72


class RLLevel(djm.IntegerChoices):
    WOOD = 0, "wood"
    BRONZE = 1, "bronze"
    SILVER = 2, "silver"
    GOLD = 3, "gold"
    PLATINUM = 4, "platinum"
    DIAMOND = 5, "diamond"
    MASTER = 6, "master"


WOOD_VALUE = 1.5
MASTER_VALUE = 0.5
MASTER_TO_WOOD_SLOPE = (WOOD_VALUE - MASTER_VALUE) / len(RLLevel.choices)


class RocketLeagueManager(djm.Manager):
    def get_queryset(self):
        """Overrides the djm.Manager method"""
        return (
            super()
            .get_queryset()
            .annotate(
                total_points=djm.ExpressionWrapper(
                    (djm.F("score") * djm.Value(POINTS_PER_POINT) + djm.F("got_mvp") * djm.Value(POINTS_PER_MVP))
                    * (djm.F("did_win") * djm.Value(1 - LOSS_SCALAR) + djm.Value(LOSS_SCALAR))
                    * (djm.Value(WOOD_VALUE) - djm.F("level") * djm.Value(MASTER_TO_WOOD_SLOPE)),
                    output_field=djm.IntegerField(),
                )
            )  # end annotate
        )  # end return


class RocketLeague(djm.Model):
    user = djm.ForeignKey(User, on_delete=djm.CASCADE)
    datetime = djm.DateTimeField(auto_now_add=True)

    score = djm.IntegerField("End Game Score", default=0)
    level = djm.IntegerField("Level", default=RLLevel.GOLD, choices=RLLevel.choices)
    got_mvp = djm.BooleanField("Got MVP?", default=False)
    did_win = djm.BooleanField("Did you win?", default=False)

    # manager
    objects = RocketLeagueManager()

    # for forms
    bool_fields = ["got_mvp", "did_win"]
    upload_fields = ["score", "level", *bool_fields]

    def __str__(self):
        try:
            return f"{self.user} @ {self.datetime:%b-%d %H:%M} == {self.total_points:,.0f}"
        except AttributeError:
            pass
        return f"{self.user} @ {self.datetime:%b-%d %H:%M}"
