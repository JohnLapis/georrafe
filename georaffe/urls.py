from django.urls import path

from . import views

app_name = "georaffe"

urlpatterns = [
    path("geocode/json", views.geocode),
    path("reverse_geocode/json", views.reverse_geocode),
]
