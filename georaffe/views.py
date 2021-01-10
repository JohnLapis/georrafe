import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

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


def parse_geocode_data(data):
    return {
        "results": [
            {"location": res["geometry"]["location"]} for res in data["results"]
        ]
    }


def get_status_code(message):
    return API_RESPONSE_TABLE[message]


@require_http_methods(["GET"])
def geocode(request):
    res = requests.get(
        f"https://{API_ROOT}/json",
        params={
            "address": request.GET.get("address"),
            "key": API_KEY,
        },
    )
    data = res.json()

    if get_status_code(data["status"]) == 200:
        return JsonResponse(parse_geocode_data(data), status=200)

    return JsonResponse(
        {"status": data["status"]}, status=get_status_code(data["status"])
    )

@require_http_methods(["GET"])
def reverse_geocode(request):
    pass
