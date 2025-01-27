from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, PartViewSet, AircraftViewSet
from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()
router.register('teams', TeamViewSet)
router.register('parts', PartViewSet)
router.register('aircrafts', AircraftViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("assemble-aircraft/", views.assemble_aircraft, name="assemble_aircraft"),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.your_profile_view, name='profile'),
    path('assembled-aircraft/', views.assembled_aircraft_list, name='assembled_aircraft_list'),
    path('create-part/', views.create_part, name='create_part'),
    path('list-parts/', views.list_parts, name='list_parts'),
    path('delete-part/<int:part_id>/', views.delete_part, name='delete_part'),
    path('update_count/<int:part_id>/', views.update_count, name='update_count'),
    path('', views.home, name='home'),  # This will make the home page available at the root URL

]
