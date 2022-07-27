from pydantic import BaseModel

# Pydantic classes used to define schema of error responses in OpenAPI
class ErrorDetail(BaseModel):
    message: str
    errors: list

class ErrorResponse(BaseModel):
  detail: ErrorDetail
