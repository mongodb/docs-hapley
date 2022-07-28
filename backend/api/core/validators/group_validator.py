from pydantic import BaseModel, root_validator

from api.exceptions import ValidationError
from api.models.group import Group
from api.models.repo import Repo


class GroupValidator(BaseModel):
    repo: Repo
    group: Group

    @classmethod
    def get_version_names(cls, repo: Repo) -> set[str]:
        return set([version.git_branch_name for version in repo.versions])

    @classmethod
    def get_group_labels(cls, groups: list[Group]) -> set[str]:
        return set([group.group_label for group in groups])

    @root_validator(pre=True)
    def validate_group(cls, values):
        errors = []

        new_group: Group = values.get("group")
        new_group_label = new_group.group_label
        repo: Repo = values.get("repo")
        existing_groups: list[Group] = repo.groups

        # Every version in included branches should be in the repo's array of branches
        missing_versions = list(
            set(new_group.included_branches) - cls.get_version_names(repo)
        )
        if len(missing_versions) > 0:
            err_msg = (
                f'Attempting to use version "{",".join(missing_versions)}" in {new_group_label}, '
                f'but version "{",".join(missing_versions)}" does not exist.'
            )
            errors.append(err_msg)

        # All remaining checks depend on pre-existing groups
        if existing_groups is not None:
            # Group label should be unique
            if new_group_label in cls.get_group_labels(existing_groups):
                errors.append(f"Duplicate group label: {new_group_label}.")

            # No two groups should use the same version
            existing_included_branches = [
                group.included_branches for group in existing_groups
            ]
            flattened_existing_branches = [
                branch for branches in existing_included_branches for branch in branches
            ]
            previously_used_versions = list(
                set(new_group.included_branches) & set(flattened_existing_branches)
            )
            if len(previously_used_versions) > 0:
                err_msg = (
                    f'Attempting to use version {",".join(previously_used_versions)} in {new_group_label}. '
                    f'{",".join(previously_used_versions)} already exists in another group.'
                )
                errors.append(err_msg)
        if len(errors) > 0:
            raise ValidationError(
                f"There were errors validating a group for repo {repo.name}",
                errors,
            )
        return values
