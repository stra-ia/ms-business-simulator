from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services import feedback_services

router = APIRouter()

class FeedbackRequest(BaseModel):
    user_creative_body: str
    user_headline: str
    user_link_description: str
    days_duration: int
    spend_by_day: float
    categorical_score: str
    total_impressions: int
    user_input_impressions_over_spend: float
    brief: str

@router.post("/", response_model=dict)
async def give_feedback(request: FeedbackRequest):
    try:
        results = feedback_services.generate_feedback(
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