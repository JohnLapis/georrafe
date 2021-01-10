import pytest


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
    def test_given_existent_address(self, client, params, expected):
        res = client.get("/api/geocode/json", params)

        assert res.status_code == 200
        assert res.json() == expected

    def test_given_nonexistent_address(self, client):
        res = client.get(
            "/api/geocode/json", {"address": "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"}
        )

        assert res.status_code == 200
        assert res.json() == {"results": []}

    def test_given_invalid_address(self, client):
        res = client.get("/api/geocode/json", {"address": ""})

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
    def test_given_valid_geocode(self, client, params, expected):
        res = client.get("/api/reverse_geocode/json", params)

        assert res.status_code == 200
        assert res.json() == expected

    def test_given_nonexistent_geocode(self, client):
        res = client.get(
            "/api/reverse_geocode/json", {"latlng": "84.451090, -75.045646"}
        )

        assert res.status_code == 200
        assert res.json() == {"results": []}

    @pytest.mark.only
    def test_given_invalid_geocode(self, client):
        res = client.get("/api/geocode/json", {"latlng": ""})

        assert res.status_code == 400
        assert res.json()["status"] == "INVALID_REQUEST"
