import random
from typing import List, Annotated

from fastapi import APIRouter, FastAPI, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from service.api.exceptions import UserNotFoundError
from service.log import app_logger


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return f"I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")
    k_recs = request.app.state.k_recs

    # Write your code here
    if model_name == "random":
        reco = random.sample(range(0, 1000), k_recs)

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    return RecoResponse(user_id=user_id, items=reco)


def add_views(app: FastAPI) -> None:
    app.include_router(router)
