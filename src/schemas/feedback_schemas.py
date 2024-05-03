from pydantic import BaseModel
from typing import List
from src.schemas.chatbot_schemas import ChatMessage

class FeedbackSalesRequest(BaseModel):
    chat_history: List[ChatMessage]
    brief: str

class FeedbackMarketingRequest(BaseModel):
    user_creative_body: str
    user_headline: str
    user_link_description: str
    days_duration: int
    spend_by_day: float
    categorical_score: str
    total_impressions: int
    user_input_impressions_over_spend: float
    brief: str