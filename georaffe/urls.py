from django.urls import path

from . import views

app_name = "georaffe"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("api/geocode/json", views.Geocode.as_view(), name="geocode"),
    path(
        "api/reverse-geocode/json",
        views.ReverseGeocode.as_view(),
        name="reverse-geocode",
    ),
]
