from django.contrib import admin

from thebus.ots import models as ots_models

class StopAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',)
    search_fields = ('code', 'name',)

admin.site.register(ots_models.Stop, StopAdmin)


class RouteAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name',)
    list_filter = ('short_name', 'name',)
    search_fields = ('short_name', 'name',)

admin.site.register(ots_models.Route, RouteAdmin)

class TripAdmin(admin.ModelAdmin):
    list_display = ('headsign',)
    search_fields = ('headsign',)

admin.site.register(ots_models.Trip, TripAdmin)

class BusAdmin(admin.ModelAdmin):
    list_display = ('number', 'manufacturer', 'paint', 'model', 'is_hybrid')
    search_fields = ('number',)

admin.site.register(ots_models.Bus, BusAdmin)
