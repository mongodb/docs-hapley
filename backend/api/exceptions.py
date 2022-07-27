from fastapi import HTTPException, status


class UserNotEntitled(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not entitled to this docs content repo.",
        )


class RepoNotFound(HTTPException):
    def __init__(self, repo_name: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The repo {repo_name} does not exist.",
        )


class ValidationError(HTTPException):
    def __init__(self, message, errors: list[str]) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": message, "errors": errors},
        )


class ReorderIndexError(HTTPException):
    def __init__(self, index: int, model_name: str, repo_name: str) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Index {index} is out of bounds of {model_name} for repo: {repo_name}",
        )
