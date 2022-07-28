from pydantic import BaseModel, Field, validator

from api.exceptions import ValidationError


class Version(BaseModel):
    git_branch_name: str = Field(alias="gitBranchName")
    active: bool
    url_aliases: list[str] | None = Field(alias="urlAliases")
    publish_original_branch_name: bool | None = Field(alias="publishOriginalBranchName")
    url_slug: str | None = Field(alias="urlSlug")
    version_selector_label: str | None = Field(alias="versionSelectorLabel")
    is_stable_branch: bool | None = Field(alias="isStableBranch")

    # Pydantic type checking runs after custom validations
    # Need to verify presence of git_branch_name since downstream validations depend on it
    @validator("git_branch_name", always=True, pre=True)
    def git_branch_validator(cls, value):
        if value is None:
            raise ValidationError(
                "Version error",
                "gitBranchName is required",
            )
        return value

    @validator("url_slug", always=True)
    def url_slug_validator(cls, v, values):
        # Defaults to git branch if not specified, otherwise perform validations
        if v is None:
            return values["git_branch_name"]
        else:
            if v != values["git_branch_name"] and v not in values["url_aliases"]:
                raise ValidationError(
                    "Version error",
                    "urlSlug must match gitBranchName or be an element of url aliases",
                )
        return v

    @validator("version_selector_label", always=True)
    def version_selector_label_validator(cls, v, values):
        # Defaults to git branch if not specified
        if v is None:
            return values["git_branch_name"]
        return v
