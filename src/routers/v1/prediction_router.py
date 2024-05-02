from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.services import prediction_services

router = APIRouter()

class PredictionRequest(BaseModel):
    user_creative_body: str
    user_headline: str
    user_link_description: str
    days_duration: int
    spend_by_day: float

@router.post("/predict", response_model=dict)
async def perform_prediction(request: PredictionRequest):
    print('request')
    print(request)
    try:
        # Pass all the user inputs to the calculate_user_scores function
        results = prediction_services.calculate_user_scores(
            user_creative_body=request.user_creative_body,
            user_headline=request.user_headline,
            user_link_description=request.user_link_description,
            days_duration=request.days_duration,
            spend_by_day=request.spend_by_day
        )
        return results
    except Exception as e:
        # Handle exceptions and return an appropriate HTTP error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))