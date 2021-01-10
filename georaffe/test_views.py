import pytest


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
def test_geocode_given_existent_address(client, params, expected):
    res = client.get("/api/geocode/json", params)

    assert res.status_code == 200
    assert res.json() == expected


def test_geocode_given_nonexistent_address(client):
    res = client.get("/api/geocode/json", {"address": "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"})

    assert res.status_code == 200
    assert res.json() == {"results": []}


def test_geocode_given_invalid_address(client):
    res = client.get("/api/geocode/json", {"address": ""})

    assert res.status_code == 400
    assert res.json()["status"] == "INVALID_REQUEST"
