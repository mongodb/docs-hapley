from starlette.middleware.cors import CORSMiddleware
from api.core.config import Settings
from api.core.factory import create_app
from api.core.middleware.authorization import Authorization

settings = Settings()
app = create_app(settings)

# Add necessary middleware to the application

# Prevent CORS errors in local development
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"]
)
# Authorization based on Okta group membership
app.add_middleware(Authorization)
