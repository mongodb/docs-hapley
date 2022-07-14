from fastapi import APIRouter, Request

from ...model.entitlement import Entitlement, PersonalRepos

router = APIRouter()


@router.get("/", response_model=PersonalRepos, tags=["repos"])
async def read_repos(request: Request):
    return await Entitlement.find_one(Entitlement.email == request.state.user.email)
