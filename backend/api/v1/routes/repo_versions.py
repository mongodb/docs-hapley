from fastapi import APIRouter
from ...model.repo import RepoVersionsView, Version, find_one_repo, RepoNotFound

router = APIRouter()
ENDPOINT_URL = "/{repo_name}/versions"

@router.get(ENDPOINT_URL, response_model=RepoVersionsView, response_model_by_alias=False, tags=["versions"])
async def read_versions(repo_name: str):
  repo = await find_one_repo(repo_name)
  if not repo:
    raise RepoNotFound(repo_name)
  return repo

@router.post(ENDPOINT_URL, response_model=Version, response_model_by_alias=False, tags=["versions"])
async def create_version(repo_name: str, version: Version):
  # TODO: implement with validations
  pass

@router.put(ENDPOINT_URL, response_model=Version, response_model_by_alias=False, tags=["versions"])
async def update_version(repo_name: str, version: Version):
  # TODO: pull shared code into a dependency (after Raymund's PR)
  repo = await find_one_repo(repo_name)
  if not repo:
    raise RepoNotFound(repo_name)
  pass