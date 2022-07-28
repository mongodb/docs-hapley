from api.tests.base import FastApiTest


def groups_route(repo_name):
    return f"/repos/{repo_name}/groups/"


def get_groups(client: FastApiTest, repo_name: str):
    response = client.get(groups_route(repo_name))
    assert response.status_code == 200
    groups = response.json()["groups"]
    return groups


def post_groups(client: FastApiTest, repo_name: str, new_group: dict):
    groups = get_groups(client, repo_name)

    response = client.post(groups_route(repo_name), json=new_group)
    res_json = response.json()
    assert response.status_code == 200
    # assigned a valid object id
    assert len(res_json["id"]) > 0
    del res_json["id"]
    assert res_json == new_group

    new_groups = get_groups(client, repo_name)
    assert len(new_groups) - len(groups) == 1


def test_groups_get():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        # Existing groups
        groups = get_groups(client, "docs")
        assert len(groups) == 2


def test_groups_get_not_entitled():
    unentitled_user = "foo@gmail.com"
    with FastApiTest(email=unentitled_user) as client:
        response = client.get(groups_route("docs"))
        assert response.status_code == 401


def test_groups_get_none():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        # Nonexistent groups
        groups = get_groups(client, "docs-landing")
        assert len(groups) == 0


def test_groups_post():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        repo_name = "docs"
        new_group = {"groupLabel": "New Test Group Post", "includedBranches": []}
        post_groups(client, repo_name, new_group)


def test_groups_post_first_group():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        new_group = {"groupLabel": "New Test Group Post", "includedBranches": []}
        repo_name = "docs-landing"
        post_groups(client, repo_name, new_group)


def test_groups_post_existing_group():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        new_group = {"groupLabel": "Major Release", "includedBranches": []}

        response = client.post(groups_route("docs"), json=new_group)
        assert response.status_code == 422

        detail = response.json()["detail"]
        errs = detail["errors"]
        assert "Duplicate group label: Major Release." in errs


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
        assert "already exists in another group" in errs[0]


def test_groups_post_no_version():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        new_group = {
            "groupLabel": "New Test Group - Used Version",
            "includedBranches": ["fake-version"],
        }

        response = client.post(groups_route("docs"), json=new_group)
        assert response.status_code == 422

        detail = response.json()["detail"]
        errs = detail["errors"]
        assert len(errs) == 1
        assert 'version "fake-version" does not exist' in errs[0]


def test_groups_put():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        new_indexes = {"currentIndex": 2, "targetIndex": 0}
        repo_name = "docs"

        groups = get_groups(client, repo_name)
        response = client.put(groups_route(repo_name), json=new_indexes)
        new_groups = get_groups(client, repo_name)

        assert response.status_code == 200
        assert len(groups) == len(new_groups)
        assert groups[2] == new_groups[0]


def test_groups_put_out_of_bounds():
    entitled_user = "test@mongodb.com"
    with FastApiTest(email=entitled_user) as client:
        new_indexes = {"currentIndex": 5, "targetIndex": 0}
        repo_name = "docs"

        response = client.put(groups_route(repo_name), json=new_indexes)

        assert response.status_code == 422
        assert "Index 5 is out of bounds" in response.json()["detail"]["errors"][0]
