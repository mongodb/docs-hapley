from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, Field, validator

from api.exceptions import ValidationError


class Version(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    git_branch_name: str = Field(alias="gitBranchName")
    active: bool
    url_aliases: list[str] | None = Field(alias="urlAliases")
    publish_original_branch_name: bool | None = Field(alias="publishOriginalBranchName")
    url_slug: str | None = Field(alias="urlSlug")
    version_selector_label: str | None = Field(alias="versionSelectorLabel")
    is_stable_branch: bool | None = Field(alias="isStableBranch")

    # If validation on git_branch_name fails, it won't be included in values.
    # https://pydantic-docs.helpmanual.io/usage/validators/
    @validator("url_slug", always=True)
    def url_slug_validator(cls, v, values):
        if "git_branch_name" not in values:
            return v

        # Defaults to git branch if not specified
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
        if "git_branch_name" in values:
            if v is None:
                return values["git_branch_name"]
        return v
