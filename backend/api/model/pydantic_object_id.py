from bson import ObjectId

"""
  FastAPI only understands JSON, so we need to provide a custom wrapper around BSON ObjectIDs
  Reference: https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
"""


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object_id")
        return ObjectId(v)
