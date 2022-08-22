from django.contrib import admin
from .models import *
from .form import OpenDateForm
# Register your models here.

admin.site.register(Reservations)


class OpenDatesAdmin(admin.ModelAdmin):
    form = OpenDateForm
admin.site.register(OpenDates,OpenDatesAdmin)