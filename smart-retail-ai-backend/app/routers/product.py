from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from fastapi.concurrency import run_in_threadpool
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.services.product_service import predict_product
from app.db.session import get_db
from app.db import models
from app.routers.auth import get_current_user
from app.schemas import ProductPredictionResult

router = APIRouter(tags=["Product Classification"])

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post(
    "/classify-product",
    response_model=ProductPredictionResult,
    summary="Classify retail product category",
    description="Allows registered users to upload a photo of a clothing product and classifies it using MobileNetV2.",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Invalid image or size exceeded"},
        401: {"description": "Unauthorized"},
    }
)
async def classify_product(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Only JPEG, PNG, and WEBP images are allowed."
        )

    try:
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error reading file size."
        )

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 5MB limit."
        )

    try:
        image = Image.open(file.file)
        image.load()
    except (UnidentifiedImageError, ValueError, TypeError, OSError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file or format."
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to process the uploaded image."
        )

    # Non-blocking TensorFlow prediction run inside a thread pool
    result = await run_in_threadpool(predict_product, image)

    # Save to Database history log
    db_history = models.PredictionHistory(
        user_id=current_user.id,
        request_type="product",
        filename=file.filename,
        content_type=file.content_type,
        file_size=file_size,
        result_category=result["category"],
        result_confidence=result["confidence"]
    )
    db.add(db_history)
    db.commit()

    return result