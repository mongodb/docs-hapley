from typing import Generic, TypeVar

from pydantic import root_validator
from pydantic.generics import GenericModel

from api.exceptions import ValidationError

from ...models.payloads import ReorderItemPayload
from ...models.repo import Repo

ListT = TypeVar("ListT")


class ValidReorderPayload(GenericModel, Generic[ListT], ReorderItemPayload):
    reordering_list: list[ListT]
    repo: Repo

    @root_validator(pre=True)
    def validate_indexes(cls, values):
        for val in ReorderItemPayload.__fields__.keys():
            index = values.get(val)
            if index >= len(values.get("reordering_list")) or index < 0:
                raise ValidationError(
                    "Error reordering groups.",
                    [f"Index {index} is out of bounds."],
                )
        return values
