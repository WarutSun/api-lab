# Another user cannot read the rating of its owner.
def test_other_user_cannot_read(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    print("READ status:", res.status_code, res.text)
    assert 400 <= res.status_code <= 499
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json() == rating


# Another user cannot change the rating of its owner.
def test_other_user_cannot_update(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 1}, headers=other_auth)
    print("UPDATE status:", res.status_code, res.text)
    assert 400 <= res.status_code <= 499
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json()["stars"] == rating["stars"]


# Another user cannot delete the rating of its owner.
def test_other_user_cannot_delete(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    print("DELETE status:", res.status_code, res.text)
    assert 400 <= res.status_code <= 499
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json() == rating