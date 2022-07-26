from api.tests.base import FastApiTest


def groups_route(repo_name):
    return f"/repos/{repo_name}/groups/"


def test_groups_get():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        # Existing groups
        response = client.get(groups_route("docs"))
        assert response.status_code == 200
        groups = response.json()["groups"]
        assert len(groups) == 2


def test_groups_get_none():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        # Nonexistent groups
        response = client.get(groups_route("docs-landing"))
        assert response.status_code == 200
        groups = response.json()["groups"]
        assert groups is None


def test_groups_post():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        new_group = {"groupLabel": "New Test Group Post", "includedBranches": []}

        response = client.post(groups_route("docs"), json=new_group)
        res_json = response.json()
        assert response.status_code == 200
        assert res_json == new_group


def test_groups_post_existing():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        new_group = {"groupLabel": "Long-Term Support Release", "includedBranches": []}

        response = client.post(groups_route("docs"), json=new_group)
        assert response.status_code == 422

        detail = response.json()["detail"]
        errs = detail["errors"]
        assert "Duplicate group label: Long-Term Support Release." in errs
