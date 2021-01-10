from django.urls import path

from . import views

app_name = "georaffe"

urlpatterns = [
    path("json", views.get_geocode),
]
