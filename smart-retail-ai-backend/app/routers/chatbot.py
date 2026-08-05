from fastapi import APIRouter, Depends, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from app.services.chatbot_service import chatbot_response
from app.db.session import get_db
from app.db import models
from app.routers.auth import get_current_user
from app.schemas import ChatRequest, ChatbotResponseResult

router = APIRouter(tags=["SmartRetailAI Chatbot"])

@router.post(
    "/chat",
    response_model=ChatbotResponseResult,
    summary="Get chatbot response",
    description="Allows registered users to chat with the SmartRetailAI bot.",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Unauthorized"},
    }
)
async def chat(
    request: ChatRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Offload inference to thread pool
    result = await run_in_threadpool(chatbot_response, request.message)

    # Save chatbot conversation log
    db_chat = models.ChatbotConversation(
        user_id=current_user.id,
        message=request.message,
        response=result["response"],
        intent_tag=result["tag"]
    )
    db.add(db_chat)
    db.commit()

    return result