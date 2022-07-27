from fastapi import APIRouter, Depends
from ...core.util.base_error import ErrorResponse
from ...models.repo import (
  Version,
  find_one_version
)
router = APIRouter(dependencies=[Depends(find_one_version)], tags=["version"], responses={
  404: {"description": "The repo specified by `repo_name` or version specified by `git_branch_name` does not exist.", "model": ErrorResponse}})

ENDPOINT = "/{git_branch_name}"

@router.get(ENDPOINT, response_model=Version, description="Get details for a version")
async def read_version(version: Version = Depends(find_one_version)):
  return version

# TODO: this would break if the user edited the git branch name
# TODO: perhaps use UUID as immutable identifier for a given version
# @router.put(ENDPOINT, response_model=Version, description="Update a version")
# async def update_version(version: Version = Depends(find_one_version)):
