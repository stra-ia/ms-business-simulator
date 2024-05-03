from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services import feedback_services
from src.schemas.feedback_schemas import FeedbackMarketingRequest, FeedbackSalesRequest
import json

router = APIRouter()

@router.post("/sales", response_model=dict)
async def give_feedback_sales(request: FeedbackSalesRequest):
# async def give_feedback_sales():
    try:
        # messages = "\n".join([f"{message['role']} - {message['content']}" for message in enumerate(request.chat_history)])
        dialogue_text = ""
        for message in request.chat_history:
            # Usamos el mapeo de roles o el original si no está definido.
            role = message.role
            content = message.content
            dialogue_text += f"{role}: {content}\n\n"
        results = feedback_services.get_sales_feedback(
            brief=request.brief,
            chat_history=dialogue_text
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/marketing", response_model=dict)
async def give_feedback_marketing(request: FeedbackMarketingRequest):
    try:
        results = feedback_services.generate_marketing_feedback(
            user_creative_body=request.user_creative_body,
            user_headline=request.user_headline,
            user_link_description=request.user_link_description,
            days_duration=request.days_duration,
            spend_by_day=request.spend_by_day,
            total_impressions=request.total_impressions,
            categorical_score=request.categorical_score,
            user_input_impressions_over_spend=request.user_input_impressions_over_spend,
            brief=request.brief
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
