import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView, View

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
    def validate_latitude(lat):
        return int(lat) >= -90 and int(lat) <= 90

    @staticmethod
    def validate_longitude(lng):
        return int(lng) >= -180 and int(lng) <= 180

    @staticmethod
    def parse_data(data):
        lat, lng, *rest = data.split(",")
        try:
            if len(rest) != 0:
                raise ValueError
            self.validate_latitude(lat)
            self.validate_longitude(lng)
        except Exception:
            raise ValueError

        return (int(lat), int(lng))

    @staticmethod
    def get_geometric_distance(lat_lng1, lat_lng2):
        pass

    def get(self, request):
        try:
            lat_lng1, lat_lng2, *rest = [
                self.parse_data(value) for value in request.GET.getlist("latlng")
            ]

            if len(rest) != 0:
                raise ValueError
        except ValueError:
            return JsonResponse(
                {"status": "INVALID_REQUEST"},
                status=get_status_code("INVALID_REQUEST"),
            )

        distance = self.get_geometric_distance(lat_lng1, lat_lng2)
        return JsonResponse({"result": distance}, status=200)
