import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Boundary values: 1 and 5 are saved, 0 and 6 are refused and change nothing.
@pytest.mark.parametrize(
    "stars, expected_status",
    [(0, 400), (1, 200), (5, 200), (6, 400)],
)
def test_update_stars_boundaries(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status
    if expected_status == 400:
        assert res.json() == {"error": STARS_ERROR}
        saved = rating["stars"]
    else:
        saved = stars
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json()["stars"] == saved