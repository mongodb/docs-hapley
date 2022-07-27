from api.core.config import get_settings
from api.core.factory import create_app
from api.database import start_db_client
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import fastapi.openapi.utils as fu
from fastapi import status

settings = get_settings()
app = create_app(settings)


@app.on_event("startup")
async def startup_app():
    await start_db_client(settings)

# Override default exception handler to ensure consistent error responses
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": {"message": "Encountered a validation error", "errors": exc.errors()}}),
    )

# Reflect the overriden exception handler in the docs
fu.validation_error_response_definition = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "detail": {"type": "object", "properties": {"message": {"type": "string"}, "errors": {"type": "array", "items": {}}}},
    },
}