def test_rain_code_membership():
    rain_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82]
    assert 61 in rain_codes

def test_snow_code_membership():
    snow_codes = [71, 73, 75, 77, 85, 86]
    assert 71 in snow_codes
    