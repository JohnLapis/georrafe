from django.urls import path

from . import views

app_name = "georaffe"

urlpatterns = [
    path("geocode/json", views.Geocode.as_view(), name="geocode"),
    path(
        "reverse_geocode/json",
        views.ReverseGeocode.as_view(),
        name="reverse_geocode",
    ),
]
