from typing import Generic, TypeVar

from beanie import Document
from pydantic import BaseModel, Field, root_validator, validator
from pydantic.generics import GenericModel

from api.exceptions import ValidationError

from .group import Group
from .payloads import ReorderItemPayload
from .version import Version


class Repo(Document):
    """Representation of a docs content repo."""

    name: str = Field(alias="repoName")
    versions: list[Version] = Field(alias="branches")
    groups: list[Group] | None

    class Settings:
        name = "repos_branches"


class RepoGroupsView(BaseModel):
    """Projection focused on groups for a specific repo."""

    groups: list[Group] | None

    @validator("groups")
    def validate_groups(cls, groups: list[Group] | None) -> list[Group]:
        return groups or []


class RepoVersionsView(BaseModel):
    """Projection focused on versions for a specific repo."""

    versions: list[Version] = Field(alias="branches")


class VersionPayloadWithRepo(BaseModel):
    version: Version
    repo: Repo
    
    @classmethod
    def validate_unique_git_branch_name(cls, new_version, existing_versions):
        if new_version.git_branch_name in [
            version.git_branch_name for version in existing_versions
        ]:
            return f"gitBranchName: {new_version.git_branch_name } is already in use"

    @classmethod
    def validate_unique_url_aliases(cls, new_version, existing_versions):
        alias_errors = []
        new_aliases = new_version.url_aliases
        if new_aliases is not None:
            existing_aliases = filter(
                None, [version.url_aliases for version in existing_versions]
            )
            for aliases in existing_aliases:
                if set(new_version.url_aliases) & set(aliases):
                    alias_errors.append(f"urlAliases: one of {new_aliases} is already in use")
        return alias_errors

    @classmethod
    def validate_single_stable_branch(cls, new_version, existing_versions):
        if new_version.is_stable_branch:
            num_stable_branches = len(
                list(filter(lambda version: version.is_stable_branch, existing_versions))
            )
            if num_stable_branches > 0:
                return "Only one stable branch can be present"

    @classmethod
    def validate_unique_version_selector(cls, new_version, existing_versions):
        version_selector_label = new_version.version_selector_label
        if version_selector_label is not None:
            if version_selector_label in set(
                [version.version_selector_label for version in existing_versions]
            ):
                return f"versionSelectorLabel: {version_selector_label} is already in use"

    @root_validator(pre=True)
    def validate_version(cls, values):
        errors = []
        new_version: Version = values.get("version")
        list_versions: list[Version] = values.get("repo").versions

        errors.append(cls.validate_unique_git_branch_name(new_version, list_versions))
        errors.extend(cls.validate_unique_url_aliases(new_version, list_versions))
        errors.append(cls.validate_single_stable_branch(new_version, list_versions))
        errors.append(cls.validate_unique_version_selector(new_version, list_versions))

        errors = [error for error in errors if error is not None]
        if len(errors) > 0:
            raise ValidationError(
                f"There were errors validating a version for repo {values.get('repo').name}",
                errors,
            )
        return values


class GroupValidator:
    def __init__(self, repo: Repo) -> None:
        self.repo = repo
        self.seen_versions: dict[str, str] = {}
        self.seen_labels: set[str] = set()
        self.errors: list[str] = []
        self.existing_versions: set[str] = self.get_version_names()

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


ListT = TypeVar("ListT")


class ReorderPayloadWithList(GenericModel, Generic[ListT], ReorderItemPayload):
    reorderingList: list[ListT]
    repo: Repo

    @root_validator(pre=True)
    def validate_indexes(cls, values):
        print(ReorderItemPayload.__fields__.keys())
        for val in ReorderItemPayload.__fields__.keys():
            index = values.get(val)
            print(index)
            if index >= len(values.get("reorderingList")) or index < 0:
                raise ValidationError(
                    "Error reordering groups.",
                    [f"Index {index} is out of bounds."],
                )
        return values


async def insert_new_group(repo: Repo, group: Group) -> None:
    validator = GroupValidator(repo)
    validator.validate_new_group(group)
    await repo.update({"$push": {"groups": group}})


async def reorder_groups(repo: Repo, current_index: int, target_index: int) -> None:
    """
    Accepts the current index of the group to move and then moves it to the target
    index.
    """

    groups = repo.groups

    max_index = max(current_index, target_index)
    if max_index >= len(groups):
        raise ValidationError(
            "Error reordering groups.",
            [f"Index {max_index} is out of bounds."],
        )

    if current_index == target_index:
        return

    group_to_move = groups.pop(current_index)
    groups.insert(target_index, group_to_move)

    validator = GroupValidator(repo)
    validator.validate_new_groups(groups)
    await repo.update({"$set": {"groups": groups}})


async def insert_new_version(repo: Repo, version: Version) -> Repo:
    await repo.update({"$push": {"branches": version}})
    return repo


async def reorder_repo_version(
    repo: Repo, current_index: int, target_index: int
) -> Repo:
    repo.versions.insert(target_index, repo.versions.pop(current_index))
    await repo.update({"$set": {"branches": repo.versions}})
    return repo
