import pytest


# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize(
    "excluded",
    [
        [],
        ["Knife"],
        ["Scissors"],
        ["Knife", "Pizza cutter"],
    ],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# A request that no pizza can satisfy is refused with 400 and a JSON error.
@pytest.mark.xfail(
    reason="Defect 1: excluding all three tools gives 500 with an empty body instead of 400 with a JSON error",
    strict=True,
)
def test_all_tools_excluded_is_refused(api, auth):
    body = {"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()