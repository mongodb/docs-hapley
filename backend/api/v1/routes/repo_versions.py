from fastapi import APIRouter, Depends
from ...model.repo import RepoVersionsView, Repo, reorder_validator, ReorderVersionValidator, ReorderPayload, Version, reorder_version, find_one_repo, RepoNotFound

router = APIRouter(dependencies=[Depends(find_one_repo)])
ENDPOINT_URL = "/{repo_name}/versions"


@router.get(ENDPOINT_URL, response_model=RepoVersionsView, tags=["versions"])
async def read_versions(repo: Repo = Depends(find_one_repo)):
  return repo

# Create a new version
@router.post(ENDPOINT_URL, response_model=Version, response_model_by_alias=False, tags=["versions"])
async def create_version(version: Version, repo: Repo = Depends(find_one_repo)):
  # TODO: implement with validations
  pass

# Reorder the positions of the versions
# Not a swap, but a reorder
"""
  Expected body: {
    "currIndex":
    "newIndex":
  }
"""
# @router.put(ENDPOINT_URL, response_model=RepoVersionsView, response_model_by_alias=False, tags=["versions"])
# async def update_version(repo_name: str, orderedVersions: ReorderPayload):
#   updated_repo = await reorder_version(repo_name, orderedVersions)
#   return updated_repo

# async def reordering_parameters
#   repo: Repo = await find_one_repo(repo_name)
#   ReorderVersionValidator(repo, orderedVersions).validate()
#   return { "repo": repo, "orderedVersions": orderedVersions }

@router.put(ENDPOINT_URL, response_model=RepoVersionsView, response_model_by_alias=False, tags=["versions"])
async def update_version(reorder_params: dict = Depends(reorder_validator)):
  updated_repo = await reorder_version(reorder_params['repo'], reorder_params['currIndex'], reorder_params['newIndex'])
  return updated_repo
