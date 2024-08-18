from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, delete

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate, ItemOut, ItemsOut, ItemUpdate, Message, Interaction, InteractionType, RecommendationOut, RecommendationsOut, ExplainationOut

router = APIRouter()

@router.get("/", response_model=RecommendationsOut)
def read_recommendations(
    session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Retrieve recommended items and explains about recommendation.
    """
    recommendations = [
        {
            "rec_item_id": 54,
            "explanations": [
                {
                    "item_id": 75,
                    "interaction_type": 0
                },
                {
                    "item_id": 563,
                    "interaction_type": 2
                }
            ]
        },
        {
            "rec_item_id": 7865,
            "explanations": [
                {
                    "item_id": 546,
                    "interaction_type": 0
                },
                {
                    "item_id": 3836,
                    "interaction_type": 1
                }
            ]
        }
    ]
    for rec in recommendations:
        statement = select(Item).where(Item.id == rec["rec_item_id"])
        rec_item = session.exec(statement).one_or_none()
        rec["rec_item_name"] = rec_item.title if rec_item else "Unknown"

        for exp in rec["explanations"]:
            statement = select(Item).where(Item.id == exp["item_id"])
            exp_item = session.exec(statement).one_or_none()
            exp["item_name"] = exp_item.title if exp_item else "Unknown"
    count = len(recommendations)

    return RecommendationsOut(data=recommendations, count=count)

