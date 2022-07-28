from typing import Generic, TypeVar

from pydantic import root_validator
from pydantic.generics import GenericModel

from api.exceptions import ValidationError

from ...models.payloads import ReorderItemPayload
from ...models.repo import Repo

ListT = TypeVar("ListT")


class ReorderPayloadValidator(GenericModel, Generic[ListT], ReorderItemPayload):
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
