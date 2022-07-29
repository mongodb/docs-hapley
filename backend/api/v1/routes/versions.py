from fastapi import APIRouter, Depends, status

from api.core.validators.valid_reorder_payload import ValidReorderPayload
from api.core.validators.valid_version import ValidVersion
from api.dependencies import (
    find_one_repo,
    new_version_validator,
    reorder_version_validator,
)
from api.exceptions import ErrorResponse

from ...models.repo import (
    Repo,
    RepoVersionsView,
    insert_new_version,
    reorder_repo_version,
)
from ...models.version import Version

VERSIONS_INDEX_PATH = "/"

router = APIRouter(
    dependencies=[Depends(find_one_repo)],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Repo not found.",
            "model": ErrorResponse,
        },
    },
)


@router.get(
    VERSIONS_INDEX_PATH,
    response_model=RepoVersionsView,
    description="Get all versions for a specific repo",
)
async def read_versions(repo: Repo = Depends(find_one_repo)):
    return repo


@router.post(
    VERSIONS_INDEX_PATH,
    response_model=Version,
    description="Create a new version for a specific repo",
)
async def create_version(
    new_version_params: ValidVersion = Depends(new_version_validator),
):
    new_version = await insert_new_version(
        repo=new_version_params.repo, version=new_version_params.version
    )
    return new_version


@router.put(
    VERSIONS_INDEX_PATH,
    response_model=RepoVersionsView,
    description="Move a version to a new position in the list",
)
async def reorder_version(
    reorder_params: ValidReorderPayload = Depends(reorder_version_validator),
):
    updated_repo = await reorder_repo_version(
        repo=reorder_params.repo,
        current_index=reorder_params.current_index,
        target_index=reorder_params.target_index,
    )
    return updated_repo
