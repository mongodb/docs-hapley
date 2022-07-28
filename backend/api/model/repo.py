from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, Field, validator

from api.exceptions import ReorderIndexError, RepoNotFound, ValidationError


class PersonalRepos(BaseModel):
    repos: list[str]


class Version(BaseModel):
    git_branch_name: str = Field(alias="gitBranchName")


class Group(BaseModel):
    """A group of versions."""

    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    group_label: str = Field(alias="groupLabel")
    included_branches: list[str] = Field(alias="includedBranches")


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


async def find_one_repo(repo_name: str) -> Repo | None:
    repo = await Repo.find_one(Repo.name == repo_name)
    return repo


async def insert_new_group(repo_name: str, group: Group) -> None:
    repo = await find_one_repo(repo_name)

    if not repo:
        raise RepoNotFound(repo_name)

    validator = GroupValidator(repo)
    validator.validate_new_group(group)
    await repo.update({"$push": {"groups": group}})


async def reorder_groups(repo_name: str, current_index: int, target_index: int) -> None:
    """
    Accepts the current index of the group to move and then moves it to the target
    index.
    """

    repo = await find_one_repo(repo_name)

    if not repo:
        raise RepoNotFound(repo_name)

    groups = repo.groups
    model_name = "groups"

    max_index = max(current_index, target_index)
    if max_index >= len(groups):
        raise ReorderIndexError(max_index, model_name, repo.name)

    if current_index == target_index:
        return

    group_to_move = groups.pop(current_index)
    groups.insert(target_index, group_to_move)

    validator = GroupValidator(repo)
    validator.validate_new_groups(groups)
    await repo.update({"$set": {"groups": groups}})
