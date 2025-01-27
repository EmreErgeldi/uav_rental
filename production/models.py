from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    responsibility = models.CharField(
        max_length=20,
        choices=[('Wing', 'Wing'), ('Fuselage', 'Fuselage'), ('Tail', 'Tail'), ('Avionics', 'Avionics'), ('Assembly', 'Assembly')]
    )

    def __str__(self):
        return self.name

class Part(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=20,
        choices=[('Wing', 'Wing'), ('Fuselage', 'Fuselage'), ('Tail', 'Tail'), ('Avionics', 'Avionics')],
    )
    aircraft = models.CharField(
        max_length=20,
        choices=[('TB2', 'TB2'), ('TB3', 'TB3'), ('AKINCI', 'AKINCI'), ('KIZILELMA', 'KIZILELMA')],
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} - {self.aircraft}"

class Aircraft(models.Model):
    name = models.CharField(max_length=20, unique=True)
    wing = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, related_name='wing_parts')
    fuselage = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, related_name='fuselage_parts')
    tail = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, related_name='tail_parts')
    avionics = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, related_name='avionics_parts')
    assembled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

