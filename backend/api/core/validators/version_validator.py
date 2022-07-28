from pydantic import BaseModel, root_validator

from api.exceptions import ValidationError
from api.models.repo import Repo
from api.models.version import Version


class VersionValidator(BaseModel):
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
                    alias_errors.append(
                        f"urlAliases: one of {new_aliases} is already in use"
                    )
        return alias_errors

    @classmethod
    def validate_single_stable_branch(cls, new_version, existing_versions):
        if new_version.is_stable_branch:
            num_stable_branches = len(
                list(
                    filter(lambda version: version.is_stable_branch, existing_versions)
                )
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
                return (
                    f"versionSelectorLabel: {version_selector_label} is already in use"
                )

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
