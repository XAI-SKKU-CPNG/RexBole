from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, delete

from app.api.deps import CurrentUser, SessionDep
from app.models import Item, ItemCreate, ItemOut, ItemsOut, ItemUpdate, Message, Interaction, InteractionType, RecommendationOut, RecommendationsOut, ExplainationOut

from app.libs.ReXBole.rec_ex_api import get_rec_exp_scores

router = APIRouter()


@router.get("/", response_model=RecommendationsOut)
def read_recommendations(
    session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Retrieve recommended items and explains about recommendation.
    """

    user_inputs = {
        'model': 'LXR',
        # 'recommender':'MacridVAE-Sep-08-2024_21-06-08.pth',
        'recommender': 'CDAE-Nov-14-2024_11-40-20.pth',
        'lr': 0.01,
        'train_batch_size': 7
    }
    user_id = 20
    user_rec_scores, explanation_scores, user_interaction, items_df = get_rec_exp_scores(
        user_inputs, user_id)
    """
    ml-100k 기준
    
    user_rec_scores     : [num_items(1683)], (float, [0,1])
    explanation_scores  : [num_items(1683)], (float, [0,1])
    user_interaction    : [num_interactions,] (int, item_id)
    items_df            : items_df[item_id]로 접근
    """

    sorted_user_rec_scores = sorted(
        enumerate(user_rec_scores), key=lambda x: x[1])
    sorted_explanation_scores = sorted(
        enumerate(explanation_scores), key=lambda x: x[1])
    rec_num = 6
    exp_num = 3
    recommendations = []
    for rec_idx in range(rec_num):
        rec_item_id, rec_score = sorted_user_rec_scores[rec_idx]

        rec_item = {}
        rec_item['rec_item_id'] = rec_item_id
        print(items_df, rec_item_id)
        rec_item_name = (items_df[items_df['item_id'] == str(rec_item_id)+'.0'])[
            'title'].iloc[0]
        rec_item['rec_item_name'] = rec_item_name
        rec_item['rec_item_imageURL'] = (items_df[items_df['item_id'] == str(
            rec_item_id)+'.0'])['imageURL'].iloc[0]
        # rec_item['rec_item_price'] = (items_df[items_df['item_id'] == str(
        #     rec_item_id)+'.0'])['price'].iloc[0]
        explanations = []

        for exp_idx in range(exp_num):
            explanation = {}
            interaction_item_id = user_interaction[exp_idx]
            explanation_item_id, _ = sorted_explanation_scores[interaction_item_id]
            explanation['item_id'] = explanation_item_id
            explanation['interaction_type'] = 1
            explanation['item_name'] = (items_df[items_df['item_id'] == str(
                explanation_item_id)+'.0'])['title'].iloc[0]
            explanation['imageURL'] = (items_df[items_df['item_id'] == str(
                explanation_item_id)+'.0'])['imageURL'].iloc[0]
            # explanation['price'] = (items_df[items_df['item_id'] == str(
            #     explanation_item_id)+'.0'])['price'].iloc[0]
            explanations.append(explanation)
        rec_item['explanations'] = explanations

        recommendations.append(rec_item)
    # recommendations = [
    #     {
    #         "rec_item_id": 54,
    #         "explanations": [
    #             {
    #                 "item_id": 75,
    #                 "interaction_type": 0
    #             },
    #             {
    #                 "item_id": 563,
    #                 "interaction_type": 2
    #             }
    #         ]
    #     },
    #     {
    #         "rec_item_id": 7865,
    #         "explanations": [
    #             {
    #                 "item_id": 546,
    #                 "interaction_type": 0
    #             },
    #             {
    #                 "item_id": 3836,
    #                 "interaction_type": 1
    #             }
    #         ]
    #     }
    # ]

    count = len(recommendations)
    print(recommendations)

    return RecommendationsOut(data=recommendations, count=count)
