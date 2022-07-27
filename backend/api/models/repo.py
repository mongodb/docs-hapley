from typing import Generic, TypeVar

from beanie import Document
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, Field, root_validator, validator
from pydantic.generics import GenericModel


class PersonalRepos(BaseModel):
    """Projection of the repos accessible to the user"""

    repos: list[str]


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
        # TODO: incorporate calls to GitHub API to verify that the branch exists
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


class Group(BaseModel):
    """A group of versions."""

    group_label: str = Field(alias="groupLabel")
    included_branches: list[str] = Field(alias="includedBranches")


class DefaultRepoFields:
    """Default fields for a repo document and its views."""

    name: str = Field(alias="repoName")
    versions: list[Version] = Field(alias="branches")
    groups: list[Group] | None


class Repo(Document):
    """Representation of a docs content repo."""

    name: str = DefaultRepoFields.name
    versions: list[Version] = DefaultRepoFields.versions
    groups: list[Group] | None

    class Settings:
        name = "repos_branches"


class RepoGroupsView(BaseModel):
    """Projection focused on groups for a specific repo."""

    groups: list[Group] | None


class RepoVersionsView(BaseModel):
    """Projection focused on versions for a specific repo."""

    versions: list[Version] = DefaultRepoFields.versions


class ReorderPayload(BaseModel):
    currIndex: int
    newIndex: int


# Generic class for validating reordering of a list of items
# Can be used across branches, groups, and versions within groups
# Would be better to inherit from ReorderPayload, but then we wouldn't have access to
# reordering list because of the field definition order.
ListT = TypeVar("ListT")


class ReorderPayloadWithList(GenericModel, Generic[ListT], ReorderPayload):
    reorderingList: list[ListT]
    repo: Repo

    @root_validator(pre=True)
    def validate_indexes(cls, values):
        vals = ["currIndex", "newIndex"]
        for val in vals:
            index = values.get(val)
            if index >= len(values.get("reorderingList")) or index < 0:
                raise ValidationError(
                    "Reordering error", [f"{val}: {index} is out of range"]
                )
        return values


class VersionPayloadWithRepo(BaseModel):
    version: Version
    repo: Repo

    # TODO: break this up into helper functions
    @root_validator(pre=True)
    def validate_version(cls, values):
        errors = []
        new_version: Version = values.get("version")
        list_versions: list[Version] = values.get("repo").versions
        
        # git branch name must be unique within the repo
        new_branch_name = new_version.git_branch_name
        if new_branch_name in set(
            map(lambda version: version.git_branch_name, list_versions)
        ):
            errors.append(f"gitBranchName: {new_branch_name} is already in use")
        
        # url aliases (optional field) must be unique within the repo
        new_aliases = new_version.url_aliases
        if new_aliases is not None:
            existing_aliases = filter(None, map(lambda version: version.url_aliases, list_versions))
            for aliases in existing_aliases:
                if set(new_version.url_aliases) & set(aliases):
                    errors.append(f"urlAliases: one of {new_aliases} is already in use")
        
        # ensure only one stable branch is present
        is_stable = new_version.is_stable_branch
        if is_stable is not None:
            if (
                is_stable
                and len(
                    list(
                        filter(lambda version: version.is_stable_branch, list_versions)
                    )
                )
                >= 1
            ):
                errors.append(f"Only one stable branch can be present")

        # ensure version selector label is unique within the repo if present
        version_selector_label = values.get("version").version_selector_label
        if version_selector_label is not None:
            if version_selector_label in set(
                map(lambda version: version.version_selector_label, list_versions)
            ):
                errors.append(
                    f"versionSelectorLabel: {version_selector_label} is already in use"
                )
        if len(errors) > 0:
            raise ValidationError(
                f"There were errors validating a version for repo {values.get('repo').name}",
                errors,
            )
        return values


class RepoNotFound(HTTPException):
    def __init__(self, repo_name: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Repo not found", "errors": [f"The repo {repo_name} does not exist."]},
        )


# TODO: This is confusing OpenAPI since Pydantic has the same class name.
# We should align response to be same as Pydantic so the frontend handles errors consistently.
class ValidationError(HTTPException):
    def __init__(self, message, errors: list[str]) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": message, "errors": errors},
        )


class ReorderVersionValidator:
    def __init__(self, repo: Repo, reordering: ReorderPayload) -> None:
        self.repo: Repo = repo
        self.reordering: ReorderPayload = reordering
        self.errors: list[str] = []

    def raise_errors(self) -> None:
        if self.errors:
            raise ValidationError(
                f'There were errors validating groups for repo "{self.repo.name}".',
                self.errors,
            )

    def check_out_of_bounds(self) -> None:
        return (
            self.reordering.currIndex >= len(self.repo.versions)
            or self.reordering.newIndex >= len(self.repo.versions)
            or self.reordering.currIndex < 0
            or self.reordering.newIndex < 0
        )

    def validate(self) -> None:
        # Ensure indexes are different
        if self.reordering.currIndex == self.reordering.newIndex:
            self.errors.append(
                f"The current index ({self.reordering.currIndex}) and new index ({self.reordering.newIndex}) are the same."
            )
        # Ensure indexes are in range
        if self.check_out_of_bounds():
            self.errors.append(
                f"The current index ({self.reordering.currIndex}) or new index ({self.reordering.newIndex}) is out of range."
            )
        self.raise_errors()


class GroupValidator:
    def __init__(self, repo: Repo) -> None:
        self.repo: Repo = repo
        self.seen_versions: dict[str, str] = {}
        self.seen_labels: set[str] = set()
        self.errors: list[str] = []
        self.existing_versions: set[str] = self.get_version_names()

    # TODO: this could be in a shared Validator parent class
    def raise_errors(self) -> None:
        if self.errors:
            raise ValidationError(
                f'There were errors validating groups for repo "{self.repo.name}".',
                self.errors,
            )

    def get_version_names(self) -> set[str]:
        """Returns a set of all version names."""

        res = set()

        for version in self.repo.versions:
            res.add(version.git_branch_name)

        return res

    def validate_one_group(self, group: Group) -> None:
        """
        Validates a single group based on other groups that have already been
        validated.
        """

        group_label = group.group_label

        # Ensure that the group label is unique
        if group_label in self.seen_labels:
            self.errors.append(f"Duplicate group label: {group_label}.")
        else:
            self.seen_labels.add(group_label)

        for version in group.included_branches:
            # Ensure that every version exists in the repo's array of branches/versions
            if version not in self.existing_versions:
                err_msg = (
                    f'Attempting to use version "{version}" in {group_label}, '
                    f'but version "{version}" does not exist.'
                )
                self.errors.append(err_msg)

            # Ensure that no two groups use the same version
            if version in self.seen_versions:
                err_msg = (
                    f'Attempting to use version "{version}" in {group_label}. '
                    f"Version already used in: {self.seen_versions[version]}."
                )
                self.errors.append(err_msg)
            else:
                self.seen_versions[version] = group_label

    def validate_new_groups(self, new_groups: list[Group]) -> None:
        """
        Validates new list of groups to ensure that their data are correct. The
        new list of groups are expected to replace the existing groups.
        """

        if not new_groups:
            return

        # Since the new groups will replace the existing ones, we only need to validate against the new groups.
        for group in new_groups:
            self.validate_one_group(group)
        self.raise_errors()

    def validate_new_group(self, new_group: Group):
        """
        Validates a new group along with the existing groups to ensure that
        their data are correct.
        """

        if not new_group:
            return

        if self.repo.groups:
            for group in self.repo.groups:
                self.validate_one_group(group)

        self.validate_one_group(new_group)
        self.raise_errors()


async def find_one_repo(repo_name: str) -> Repo:
    repo = await Repo.find_one(Repo.name == repo_name)
    if not repo:
        raise RepoNotFound(repo_name)
    return repo


async def reorder_validator(
    reordering: ReorderPayload, repo: Repo = Depends(find_one_repo)
) -> None:
    return ReorderPayloadWithList[Version](
        repo=repo,
        reorderingList=repo.versions,
        currIndex=reordering.currIndex,
        newIndex=reordering.newIndex,
    )


async def new_version_validator(
    new_version: Version, repo: Repo = Depends(find_one_repo)
) -> dict[str, Repo | Version]:
    return VersionPayloadWithRepo(version=new_version, repo=repo)


async def insert_new_version(repo: Repo, version: Version) -> Repo:
    await repo.update({"$push": {"branches": version}})
    return repo


async def reorder_repo_version(
    repo: Repo, currIndex: int, newIndex: int
) -> Repo:
    repo.versions.insert(newIndex, repo.versions.pop(currIndex))
    await repo.update({"$set": {"branches": repo.versions}})
    return repo


async def insert_new_group(repo_name: str, group: Group) -> None:
    repo = await find_one_repo(repo_name)

    if not repo:
        raise RepoNotFound(repo_name)

    validator = GroupValidator(repo)
    validator.validate_new_group(group)
    await repo.update({"$push": {"groups": group}})


async def set_groups(repo_name: str, groups: list[Group]) -> None:
    repo = await find_one_repo(repo_name)

    if not repo:
        raise RepoNotFound(repo_name)

    validator = GroupValidator(repo)
    validator.validate_new_groups(groups)
    await repo.update({"$set": {"groups": groups}})
