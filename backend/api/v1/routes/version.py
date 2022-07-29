from bson import ObjectId
from fastapi import APIRouter, Depends, status

from api.core.validators.valid_version import ValidVersion
from api.dependencies import (
    convert_to_object_id,
    find_one_repo,
    find_one_version,
    update_version_validator,
)
from api.exceptions import ErrorResponse
from api.models.payloads import DeleteItemResponse
from api.models.repo import Repo, delete_repo_version, update_repo_version

from ...models.version import Version

router = APIRouter(
    dependencies=[Depends(find_one_version)],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Version not found.",
            "model": ErrorResponse,
        },
    },
)

VERSION_INDEX_PATH = "/"


@router.get(
    VERSION_INDEX_PATH, response_model=Version, description="Get a specific version"
)
async def read_version(version: Version = Depends(find_one_version)):
    return version


@router.put(
    VERSION_INDEX_PATH, response_model=Version, description="Update a specific version"
)
async def update_version(
    updated_version_params: ValidVersion = Depends(update_version_validator),
):
    await update_repo_version(
        repo=updated_version_params.repo, version=updated_version_params.version
    )
    return updated_version_params.version


@router.delete(
    VERSION_INDEX_PATH,
    response_model=DeleteItemResponse,
    description="Delete a specific version",
)
async def delete_version(
    version_id: ObjectId = Depends(convert_to_object_id),
    repo: Repo = Depends(find_one_repo),
):
    await delete_repo_version(repo=repo, version_id=version_id)
    return DeleteItemResponse(success=True, message="Version deleted successfully")
