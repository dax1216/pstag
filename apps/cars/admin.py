from django.contrib import admin

from . import models


@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["name", "color", "length", "weight"]