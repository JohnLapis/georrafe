from django.urls import path

from . import views

app_name = "georaffe"

urlpatterns = [
    path("geocode/json", views.Geocode.as_view()),
    path("reverse_geocode/json", views.reverse_geocode),
]
