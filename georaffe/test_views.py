import pytest
from django.urls import reverse

from .views import GeometricDistance


class TestGeocode:
    @pytest.mark.parametrize(
        "params,expected",
        [
            (
                {"address": "Museu de arte de São Paulo Assis Chateaubriand"},
                {"results": [{"location": {"lat": -23.561414, "lng": -46.6558819}}]},
            ),
            (
                {"address": "1600 Amphitheatre Parkway, Mountain View, CA"},
                {
                    "results": [
                        {"location": {"lat": 37.4215301, "lng": -122.0892895}},
                        {"location": {"lat": 37.4117586, "lng": -122.0837692}},
                    ]
                },
            ),
        ],
    )
    @pytest.mark.urls("georaffe.urls")
    def test_given_existent_address(self, client, params, expected):
        res = client.get(reverse("geocode"), params)

        assert res.status_code == 200
        assert res.json() == expected

    @pytest.mark.urls("georaffe.urls")
    def test_given_nonexistent_address(self, client):
        res = client.get(reverse("geocode"), {"address": "j;aoskdfha6056050jasd"})

        assert res.status_code == 200
        assert res.json() == {"results": []}

    @pytest.mark.urls("georaffe.urls")
    def test_given_invalid_address(self, client):
        res = client.get(reverse("geocode"), {"address": ""})

        assert res.status_code == 400
        assert res.json()["status"] == "INVALID_REQUEST"


class TestReverseGeocode:
    @pytest.mark.parametrize(
        "params,expected",
        [
            (
                {"latlng": "37.4215301,-122.0892895"},
                {
                    "results": [
                        {
                            "formatted_address": "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA"
                        },
                        {
                            "formatted_address": "Charleston and Huff, 223 Charleston Rd, Mountain View, CA 94043, USA"
                        },
                        {
                            "formatted_address": "223 Charleston Rd, Mountain View, CA 94043, USA"
                        },
                        {
                            "formatted_address": "1949 Charleston Rd, Mountain View, CA 94043, USA"
                        },
                        {
                            "formatted_address": "1949 Charleston Rd, Mountain View, CA 94043, USA"
                        },
                        {"formatted_address": "Mountain View, CA 94043, USA"},
                        {"formatted_address": "Mountain View, CA, USA"},
                        {
                            "formatted_address": "San Francisco Peninsula, California, USA"
                        },
                        {"formatted_address": "Santa Clara County, CA, USA"},
                        {"formatted_address": "California, USA"},
                        {"formatted_address": "United States"},
                        {"formatted_address": "CWC6+J7 Mountain View, CA, USA"},
                    ]
                },
            ),
            (
                {"latlng": "-23.561414,-46.6558819"},
                {
                    "results": [
                        {
                            "formatted_address": "Av. Paulista, 1578 - Bela Vista, São Paulo - SP, 01310-200, Brazil"
                        },
                        {
                            "formatted_address": "Av. Paulista, 1532 - Bela Vista, São Paulo - SP, 01310-200, Brazil"
                        },
                        {
                            "formatted_address": "Av. Paulista, 1578 - Bela Vista, São Paulo - SP, 01310-200, Brazil"
                        },
                        {
                            "formatted_address": "Av. Paulista, 1526 - Bela Vista, São Paulo - SP, 01310-200, Brazil"
                        },
                        {
                            "formatted_address": "Túnel 9 de Julho, 1540 - Jardim Paulista, São Paulo - SP, 01407-100, Brazil"
                        },
                        {
                            "formatted_address": "Bela Vista, São Paulo - State of São Paulo, 01332-050, Brazil"
                        },
                        {
                            "formatted_address": "São Paulo - State of São Paulo, 01332, Brazil"
                        },
                        {"formatted_address": "Bela Vista, São Paulo - SP, Brazil"},
                        {
                            "formatted_address": "Bela Vista, São Paulo - State of São Paulo, Brazil"
                        },
                        {
                            "formatted_address": "São Paulo, State of São Paulo, Brazil"
                        },
                        {
                            "formatted_address": "São Paulo - State of São Paulo, Brazil"
                        },
                        {"formatted_address": "State of São Paulo, Brazil"},
                        {"formatted_address": "Brazil"},
                        {
                            "formatted_address": "C8QV+CJ Bela Vista, São Paulo - SP, Brazil"
                        },
                    ]
                },
            ),
        ],
    )
    @pytest.mark.urls("georaffe.urls")
    def test_given_valid_geocode(self, client, params, expected):
        res = client.get(reverse("reverse-geocode"), params)

        assert res.status_code == 200
        assert res.json() == expected

    @pytest.mark.urls("georaffe.urls")
    def test_given_nonexistent_geocode(self, client):
        res = client.get(
            reverse("reverse-geocode"), {"latlng": "84.451090, -75.045646"}
        )

        assert res.status_code == 200
        assert res.json() == {"results": []}

    @pytest.mark.urls("georaffe.urls")
    def test_given_invalid_geocode(self, client):
        res = client.get(reverse("reverse-geocode"), {"latlng": ""})

        assert res.status_code == 400
        assert res.json()["status"] == "INVALID_REQUEST"


class TestGeometricDistance:
    @pytest.mark.parametrize(
        "point1,point2,expected",
        [
            (
                {"x": -122.0892895, "y": 37.4215301},
                {"x": -122.0892895, "y": 37.4215301},
                0,
            ),
            (
                {"x": 0, "y": 90},  # north pole
                {"x": 0, "y": -90},  # south pole
                # approximately, half of earth's circumference in meters
                20015086.796020572,
            ),
            (
                {"x": 180, "y": 90},  # extreme northeast
                {"x": -180, "y": -90},  # extreme southwest
                # approximately, half of earth's circumference in meters
                20015086.796020572,
            ),
            (
                {"x": -0.116773, "y": 51.510357},
                {"x": -77.009003, "y": 38.889931},
                5705124.321480648,
            ),
        ],
    )
    def test_get_geometric_distance(self, point1, point2, expected):
        distance = GeometricDistance.get_geometric_distance(point1, point2)
        assert distance == expected

    @pytest.mark.parametrize(
        "params,expected",
        [
            (
                {"latlng": ["37.4215301,-122.0892895", "37.4215301,-122.0892895"]},
                {"result": 0, "unit": "km"},
            ),
            (
                # north and south pole
                {"latlng": ["90,0", "-90,0"]},
                # approximately, half of earth's circumference in meters
                {"result": 20015.086796020572, "unit": "km"},
            ),
            (
                # extreme northeast and southwest
                {"latlng": ["90,180", "-90,-180"]},
                # approximately, half of earth's circumference in meters
                {"result": 20015.086796020572, "unit": "km"},
            ),
            (
                {"latlng": ["51.510357,-0.116773", "38.889931,-77.009003"]},
                {"result": 5705.124321480647, "unit": "km"},
            ),
        ],
    )
    @pytest.mark.urls("georaffe.urls")
    def test_given_valid_coordinates(self, client, params, expected):
        res = client.get(reverse("geometric-distance"), params)

        assert res.status_code == 200
        assert res.json() == expected

    @pytest.mark.parametrize(
        "params",
        [
            {},
            {"a": "a", "b": "b"},
            {"latlng": ["", ""]},
            {"latlng": ["37.4215301,-122.0892895", "aaaaa,bbb"]},
            {"latlng": ["37.4215301,zzzzzzzz", "aaaaa,bbb"]},
            {"latlng": ["zzzzzzzzzz,-122.0892895", "aaaaa,bbb"]},
            {
                "latlng": [
                    "37.4215301,-122.0892895,37.4215301",
                    "37.4215301,-122.0892895",
                ]
            },
            {
                "latlng": [
                    "37.4215301,-122.0892895",
                    "37.4215301,-122.0892895",
                    "37.4215301,-122.0892895",
                ]
            },
        ],
    )
    @pytest.mark.urls("georaffe.urls")
    def test_given_invalid_input(self, client, params):
        res = client.get(reverse("geometric-distance"), params)

        assert res.status_code == 400
        assert res.json()["status"] == "INVALID_REQUEST"
