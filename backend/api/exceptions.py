from fastapi import HTTPException, status
from pydantic import BaseModel


# Pydantic classes used to define schema of error responses in OpenAPI
class ErrorDetail(BaseModel):
    message: str
    errors: list


class ErrorResponse(BaseModel):
    detail: ErrorDetail


class UserNotEntitled(HTTPException):
    def __init__(self, repo_name: str) -> None:
        error: ErrorDetail = ErrorDetail(
            message="Authorization error",
            errors=[f"User is not entitled to access repo {repo_name}"],
        )
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error.dict(),
        )


class RepoNotFound(HTTPException):
    def __init__(self, repo_name: str) -> None:
        error: ErrorDetail = ErrorDetail(
            message="Repo not found.",
            errors=[f"The repo {repo_name} does not exist."],
        )
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.dict(),
        )

class VersionNotFound(HTTPException):
    def __init__(self, version_id: str) -> None:
        error: ErrorDetail = ErrorDetail(
            message="Version not found.",
            errors=[f"The version with id {version_id} does not exist."],
        )
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.dict(),
        )


class ValidationError(HTTPException):
    def __init__(self, message, errors: list[str]) -> None:
        error: ErrorDetail = ErrorDetail(
            message=message,
            errors=errors,
        )
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error.dict(),
        )
