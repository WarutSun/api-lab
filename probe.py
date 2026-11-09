import requests
import uuid

site = "https://quickpizza.grafana.com"
s = requests.Session()

user = {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}
r = s.post(site + "/api/users", json=user)
print("create user:", r.status_code)
r = s.post(site + "/api/users/token/login", json=user)
print("login:", r.status_code)
mine = {"Authorization": "token " + r.json()["token"]}
r = s.post(site + "/api/pizza", json={}, headers=mine)
print("pizza:", r.status_code)
pid = r.json()["pizza"]["id"]

cases = [
    ("stars 0", {"pizza_id": pid, "stars": 0}, mine),
    ("stars 6", {"pizza_id": pid, "stars": 6}, mine),
    ("stars decimal 3.5", {"pizza_id": pid, "stars": 3.5}, mine),
    ("stars text '3'", {"pizza_id": pid, "stars": "3"}, mine),
    ("stars missing", {"pizza_id": pid}, mine),
    ("pizza not exist", {"pizza_id": 999999999, "stars": 3}, mine),
    ("no token", {"pizza_id": pid, "stars": 3}, {}),
    ("short token", {"pizza_id": pid, "stars": 3}, {"Authorization": "token short"}),
]

for label, body, headers in cases:
    r = s.post(site + "/api/ratings", json=body, headers=headers)
    print(label, "->", r.status_code, r.text)