from django.contrib import admin
from .models import Team, Part, Aircraft

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'responsibility']

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'aircraft', 'team', 'stock']

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ['name', 'wing', 'fuselage', 'tail', 'avionics', 'assembled_at']
