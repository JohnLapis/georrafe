from math import asin, cos, radians, sin, sqrt

import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView, View

from .utils import validate_latitude, validate_longitude

API_ROOT = "maps.googleapis.com/maps/api/geocode"
API_KEY = settings.GOOGLE_GEOCODE_API_KEY
API_RESPONSE_TABLE = {
    "OK": 200,
    "ZERO_RESULTS": 200,
    "OVER_DAILY_LIMIT": 500,
    "OVER_QUERY_LIMIT": 500,
    "REQUEST_DENIED": 500,
    "UNKNOWN_ERROR": 500,
    "INVALID_REQUEST": 400,
}


def get_status_code(message):
    return API_RESPONSE_TABLE[message]


class IndexView(TemplateView):
    template_name = "index.html"


class Geocode(View):
    @staticmethod
    def parse_data(data):
        return {
            "results": [
                {"location": res["geometry"]["location"]} for res in data["results"]
            ]
        }

    def get(self, request):
        res = requests.get(
            f"https://{API_ROOT}/json",
            params={
                "address": request.GET.get("address"),
                "key": API_KEY,
            },
        )
        data = res.json()

        if get_status_code(data["status"]) == 200:
            return JsonResponse(self.parse_data(data), status=200)

        return JsonResponse(
            {"status": data["status"]}, status=get_status_code(data["status"])
        )


class ReverseGeocode(View):
    @staticmethod
    def parse_data(data):
        return {
            "results": [
                {"formatted_address": res["formatted_address"]}
                for res in data["results"]
            ]
        }

    def get(self, request):
        res = requests.get(
            f"https://{API_ROOT}/json",
            params={
                "latlng": request.GET.get("latlng"),
                "key": API_KEY,
            },
        )
        data = res.json()

        if get_status_code(data["status"]) == 200:
            return JsonResponse(self.parse_data(data), status=200)

        return JsonResponse(
            {"status": data["status"]}, status=get_status_code(data["status"])
        )


class GeometricDistance(View):
    @staticmethod
    def parse_data(data):
        lat, lng, *rest = data.split(",")
        if len(rest) != 0:
            raise ValueError
        validate_latitude(lat)
        validate_longitude(lng)

        return {"x": float(lng), "y": float(lat)}

    @staticmethod
    def get_geometric_distance(point1, point2):
        """Returns distance between two points on a sphere in meters using Haversine formula."""

        # Earth's radius in meters
        radius = 6_371_000
        # haversine function
        def hav(n):
            return sin(n / 2) ** 2

        x1, y1 = radians(point1["x"]), radians(point1["y"])
        x2, y2 = radians(point2["x"]), radians(point2["y"])

        # haversine of the central angle between the two points using coordinates
        hav_central_angle = hav(y2 - y1) ** 2 + cos(y1) * cos(y2) * hav(x2 - x1)

        # 2 * asin(sqrt(x)) is the inverse haversine of x
        central_angle = 2 * asin(sqrt(hav_central_angle))

        # since distance / radius = central angle
        return radius * central_angle

    def get(self, request):
        try:
            coord1, coord2, *rest = [
                self.parse_data(value) for value in request.GET.getlist("latlng")
            ]

            if len(rest) != 0:
                raise ValueError
        except ValueError:
            return JsonResponse(
                {"status": "INVALID_REQUEST"},
                status=get_status_code("INVALID_REQUEST"),
            )
        except Exception:
            return JsonResponse(
                {"status": "UNKNOWN_ERROR"},
                status=get_status_code("UNKNOWN_ERROR"),
            )

        distance = self.get_geometric_distance(coord1, coord2) / 1000
        return JsonResponse({"result": distance, "unit": "km"}, status=200)
