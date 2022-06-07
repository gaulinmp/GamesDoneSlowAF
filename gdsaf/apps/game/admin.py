from django.contrib import admin

# Register your models here.

from .models import Overwatch, RocketLeague

admin.site.register(Overwatch)
admin.site.register(RocketLeague)
