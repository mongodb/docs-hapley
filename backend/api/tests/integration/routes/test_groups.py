from api.tests.base import FastApiTest


def groups_route(repo_name):
    return f"/repos/{repo_name}/groups/"


def get_groups(client: FastApiTest, repo_name: str):
    response = client.get(groups_route(repo_name))
    assert response.status_code == 200
    groups = response.json()["groups"]
    return groups


def test_groups_get():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        # Existing groups
        groups = get_groups(client, "docs")
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
        repo_name = "docs"
        new_group = {"groupLabel": "New Test Group Post", "includedBranches": []}

        groups = get_groups(client, repo_name)
        assert len(groups) == 2

        response = client.post(groups_route(repo_name), json=new_group)
        res_json = response.json()
        assert response.status_code == 200
        assert res_json == new_group

        groups = get_groups(client, repo_name)
        assert len(groups) == 3


def test_groups_post_first_group():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        new_group = {"groupLabel": "New Test Group Post", "includedBranches": []}
        repo_name = "docs-landing"

        groups = get_groups(client, repo_name)
        assert groups is None

        response = client.post(groups_route(repo_name), json=new_group)
        res_json = response.json()
        assert response.status_code == 200
        assert res_json == new_group

        groups = get_groups(client, repo_name)
        assert len(groups) == 1


def test_groups_post_existing_group():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        new_group = {"groupLabel": "Long-Term Support Release", "includedBranches": []}

        response = client.post(groups_route("docs"), json=new_group)
        assert response.status_code == 422

        detail = response.json()["detail"]
        errs = detail["errors"]
        assert "Duplicate group label: Long-Term Support Release." in errs


def test_groups_post_used_version():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        new_group = {
            "groupLabel": "New Test Group - Used Version",
            "includedBranches": ["v5.0"],
        }

        response = client.post(groups_route("docs"), json=new_group)
        assert response.status_code == 422

        detail = response.json()["detail"]
        errs = detail["errors"]
        assert len(errs) == 1
        assert "Attempting to use version" in errs[0]
