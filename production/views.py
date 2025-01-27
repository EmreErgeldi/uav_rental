from rest_framework.viewsets import ModelViewSet
from .models import Team, Part, Aircraft
from .serializers import TeamSerializer, PartSerializer, AircraftSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import PartForm
from django.http import Http404
import json

class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class PartViewSet(ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class AircraftViewSet(ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

def home(request):
    return render(request, 'home.html')

@login_required
def assemble_aircraft(request):
    # Check if the user is in the 'Assembly' group and has the 'can_assemble_aircraft' permission
    print(request.user)
    if not request.user.groups.filter(name='Assembly').exists():
        return redirect('home')  # Redirect to home or show an error message
    if request.method == "POST":
        name = request.POST.get("name")
        wing_id = request.POST.get("wing")
        fuselage_id = request.POST.get("fuselage")
        tail_id = request.POST.get("tail")
        avionics_id = request.POST.get("avionics")

        # Fetch selected parts
        wing = get_object_or_404(Part, id=wing_id, type="Wing")
        fuselage = get_object_or_404(Part, id=fuselage_id, type="Fuselage")
        tail = get_object_or_404(Part, id=tail_id, type="Tail")
        avionics = get_object_or_404(Part, id=avionics_id, type="Avionics")

        # Check stock availability
        for part in [wing, fuselage, tail, avionics]:
            if part.stock <= 0:
                messages.error(request, f"{part.name} is out of stock!")
                return redirect("assemble_aircraft")

        # Reduce stock counts
        wing.stock -= 1
        fuselage.stock -= 1
        tail.stock -= 1
        avionics.stock -= 1
        wing.save()
        fuselage.save()
        tail.save()
        avionics.save()

        # Create the aircraft
        Aircraft.objects.create(
            name=name,
            wing=wing,
            fuselage=fuselage,
            tail=tail,
            avionics=avionics,
        )
        messages.success(request, "Aircraft assembled successfully!")
        return redirect("assemble_aircraft")

    # Fetch available parts
    wings = Part.objects.filter(type="Wing", stock__gt=0)
    fuselages = Part.objects.filter(type="Fuselage", stock__gt=0)
    tails = Part.objects.filter(type="Tail", stock__gt=0)
    avionics = Part.objects.filter(type="Avionics", stock__gt=0)

    context = {
        "wings": wings,
        "fuselages": fuselages,
        "tails": tails,
        "avionics": avionics,
    }
    return render(request, "assemble_aircraft.html", context)

def your_profile_view(request):
    return render(request, 'profile.html')

def assembled_aircraft_list(request):
    # Retrieve all assembled aircraft from the database
    aircrafts = Aircraft.objects.all()
    return render(request, 'assembled_aircraft_list.html', {'aircrafts': aircrafts})

@login_required
def create_part(request):
    # Check if the user belongs to the correct team
    if not request.user.groups.filter(name='Wing').exists():
        return redirect('home')  # Redirect to home or show an error message
    
    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            part = form.save(commit=False)
            part.team = request.user  # Associate the part with the current user (team)
            part.save()
            return redirect('list_parts')
    else:
        form = PartForm()
    
    return render(request, 'create_part.html', {'form': form})

@login_required
def list_parts(request):
    # List parts for the team (only parts belonging to the user's team)
    print(request.user.groups.all()[0])
    parts = Part.objects.filter(type=request.user.groups.all()[0])
    return render(request, 'list_parts.html', {'parts': parts})

@login_required
def update_count(request, part_id):
    if request.method == 'POST':
        part = Part.objects.get(id=part_id)
        part.stock = part.stock + 1
        part.save()
    return redirect('list_parts')

@login_required
def delete_part(request, part_id):
    try:
        part = Part.objects.get(id=part_id, team=request.user)
    except Part.DoesNotExist:
        raise Http404("Part does not exist")
    
    part.delete()  # Delete the part (recycle it)
    return redirect('list_parts')