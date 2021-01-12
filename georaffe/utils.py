def validate_latitude(lat):
    return float(lat) >= -90 and float(lat) <= 90


def validate_longitude(lng):
    return float(lng) >= -180 and float(lng) <= 180
