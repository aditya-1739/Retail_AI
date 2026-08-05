from fastapi import APIRouter, Depends, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from app.services.sentiment_service import analyze_sentiment
from app.db.session import get_db
from app.db import models
from app.routers.auth import get_current_user
from app.schemas import ReviewRequest, SentimentAnalysisResult

router = APIRouter(tags=["Sentiment Analysis"])

@router.post(
    "/analyze-review",
    response_model=SentimentAnalysisResult,
    summary="Analyze sentiment of text review",
    description="Allows registered users to evaluate customer review text and classify it as Positive or Negative.",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Unauthorized"},
    }
)
async def analyze(
    request: ReviewRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Offload inference to thread pool
    result = await run_in_threadpool(analyze_sentiment, request.review)

    # Save to Database history log
    db_history = models.PredictionHistory(
        user_id=current_user.id,
        request_type="sentiment",
        input_text=request.review,
        result_category=result["sentiment"],
        result_confidence=100.0
    )
    db.add(db_history)
    db.commit()

    return result