import string
from random import choices

from api.tests.base import FastApiTest

VALID_ENDPOINT: str = "/repos/docs/versions/"
INVALID_ENDPOINT: str = "/repos/foobar/versions/"


# --------- GET /repos/{repo_name}/versions ---------
def test_valid_get():
    with FastApiTest() as client:
        response = client.get(VALID_ENDPOINT)
        assert response.status_code == 200
        assert len(response.json()["branches"]) == 13
        assert response.json()["branches"][0] == {
            "publishOriginalBranchName": True,
            "active": True,
            "gitBranchName": "v4.4",
            "urlSlug": "v4.4",
            "versionSelectorLabel": "4.4",
            "urlAliases": None,
            "isStableBranch": False,
        }


def test_all_methods_invalid_repo_name():
    with FastApiTest() as client:
        http_methods = ["get", "post", "put"]
        for method in http_methods:
            response = getattr(client, method)(INVALID_ENDPOINT)
            assert response.status_code == 404
            assert (
                "The repo foobar does not exist." in response.json()["detail"]["errors"]
            )


# --------- PUT /repos/{repo_name}/versions ---------


def test_valid_put():
    with FastApiTest() as client:
        beforeUpdate = client.get(VALID_ENDPOINT).json()["branches"]
        response = client.put(
            VALID_ENDPOINT, json={"currentIndex": 0, "targetIndex": 1}
        )
        assert response.status_code == 200
        assert response.json()["branches"][1] == beforeUpdate[0]
        assert len(response.json()["branches"]) == len(beforeUpdate)


def test_invalid_payload_put():
    with FastApiTest() as client:
        invalid_values = [-1, "foo", None, 2**32]
        for value in invalid_values:
            response = client.put(
                VALID_ENDPOINT, json={"currentIndex": value, "targetIndex": 1}
            )
            assert response.status_code == 422


# --------- POST /repos/{repo_name}/versions ---------
def generate_random_valid_version():
    random_str: str = "".join(choices(string.ascii_uppercase + string.digits, k=10))
    return {
        "gitBranchName": random_str,
        "publishOriginalBranchName": True,
        "active": True,
        "urlSlug": random_str,
        "versionSelectorLabel": random_str,
        "urlAliases": [random_str],
        "isStableBranch": False,
    }


def test_valid_payload_post():
    payload = generate_random_valid_version()
    with FastApiTest() as client:
        current_num_branches = len(client.get(VALID_ENDPOINT).json()["branches"])
        response = client.post(VALID_ENDPOINT, json=payload)
        assert response.status_code == 200
        assert response.json() == payload
        new_num_branches = len(client.get(VALID_ENDPOINT).json()["branches"])
        assert new_num_branches - current_num_branches == 1


def test_invalid_git_branch_name_post():
    payload = generate_random_valid_version()
    payload["gitBranchName"] = None
    with FastApiTest() as client:
        response = client.post(VALID_ENDPOINT, json=payload)
        assert response.status_code == 422


def test_default_vals_post():
    payload = generate_random_valid_version()
    del payload["urlSlug"]
    del payload["versionSelectorLabel"]
    with FastApiTest() as client:
        response = client.post(VALID_ENDPOINT, json=payload)
        assert response.status_code == 200
        new_version = response.json()
        assert new_version["urlSlug"] == payload["gitBranchName"]
        assert new_version["versionSelectorLabel"] == payload["gitBranchName"]


def test_repeat_git_branch_name_post():
    payload = generate_random_valid_version()
    with FastApiTest() as client:
        used_branch_name = client.get(VALID_ENDPOINT).json()["branches"][0][
            "gitBranchName"
        ]
        payload["gitBranchName"] = used_branch_name
        response = client.post(VALID_ENDPOINT, json=payload)
        assert response.status_code == 422


def test_multiple_stable_branches_post():
    payload = generate_random_valid_version()
    payload["isStableBranch"] = True
    with FastApiTest() as client:
        response = client.post(VALID_ENDPOINT, json=payload)
        assert response.status_code == 422


def test_repeat_version_selector_label_post():
    payload = generate_random_valid_version()
    with FastApiTest() as client:
        used_label = client.get(VALID_ENDPOINT).json()["branches"][0][
            "versionSelectorLabel"
        ]
        payload["versionSelectorLabel"] = used_label
        response = client.post(VALID_ENDPOINT, json=payload)
        assert response.status_code == 422


def test_repeat_url_aliases_post():
    payload = generate_random_valid_version()
    payloadWithRepeat = generate_random_valid_version()
    payloadWithRepeat["urlAliases"] = payload["urlAliases"]
    with FastApiTest() as client:
        client.post(VALID_ENDPOINT, json=payload)
        response = client.post(VALID_ENDPOINT, json=payloadWithRepeat)
        assert response.status_code == 422