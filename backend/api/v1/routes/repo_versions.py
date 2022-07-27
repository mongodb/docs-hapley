from fastapi import APIRouter, Depends
from ...core.util.base_error import ErrorResponse

from ...models.repo import (
    Repo,
    RepoVersionsView,
    VersionPayloadWithRepo,
    ReorderPayloadWithList,
    find_one_repo,
    insert_new_version,
    new_version_validator,
    reorder_repo_version,
    reorder_validator,
)

router = APIRouter(dependencies=[Depends(find_one_repo)], tags=["versions"], responses={
    404: {"description": "The repo specified by `repo_name` does not exist.", "model": ErrorResponse},
})
ENDPOINT = "/{repo_name}/versions"


@router.get(
    ENDPOINT,
    response_model=RepoVersionsView,
    description="Get all versions for a specific repo",
)
async def read_versions(repo: Repo = Depends(find_one_repo)):
    return repo


@router.post(
    ENDPOINT,
    response_model=RepoVersionsView,
    description="Create a new version for a specific repo",
)
async def create_version(new_version_params: VersionPayloadWithRepo = Depends(new_version_validator)):
    with_new_version = await insert_new_version(repo=new_version_params.repo, version=new_version_params.version)
    return with_new_version


@router.put(
    ENDPOINT,
    response_model=RepoVersionsView,
    description="Moves a version to a new position in the list",
)
async def reorder_version(reorder_params: ReorderPayloadWithList = Depends(reorder_validator)):
    updated_repo = await reorder_repo_version(repo=reorder_params.repo, currIndex=reorder_params.currIndex, newIndex=reorder_params.newIndex)
    return updated_repo
