import os
import pickle
import random
from typing import List

import pandas as pd
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from rectools import Columns
from rectools.dataset import Dataset
from typing_extensions import Annotated

from service.api.exceptions import AuthenticationError, ModelNotFoundError, UserNotFoundError
from service.log import app_logger


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


load_dotenv()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
interactions_df = pd.read_csv("data_original/interactions.csv")
interactions_df.rename(columns={"last_watch_dt": Columns.Datetime, "total_dur": Columns.Weight}, inplace=True)
dataset = Dataset.construct(interactions_df)


def login(req: Request):
    token = req.headers["Authorization"]
    if token != "Bearer " + str(os.getenv("TOKEN")):
        raise AuthenticationError(error_message="Invalid token")

    return token


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
    token: Annotated[str, Depends(login)],
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    # Write your code here
    k_recs = request.app.state.k_recs
    reco = list(range(k_recs))
    if model_name == "random":
        reco = random.sample(range(1000), k_recs)
    elif model_name == "knn":
        with open("src/weights/knn_weights.pkl", "rb") as f:
            model = pickle.load(f)

        recs = model.recommend(
            users=[user_id],
            dataset=dataset,
            k=k_recs,
            filter_viewed=True,
        )
        reco = list(recs["item_id"])
    else:
        raise ModelNotFoundError(error_message=f"Model {model_name} not found")

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    return RecoResponse(user_id=user_id, items=reco)


def add_views(app: FastAPI) -> None:
    app.include_router(router)
