import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./smart_retail.db"
    SECRET_KEY: str = "supersecretkeychangeinprod123!"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALLOWED_ORIGINS: Union[str, List[str]] = ["http://localhost:5173"]
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB

    # Model and dataset paths
    CHATBOT_MODEL_PATH: str = "app/models/chatbot_model.pkl"
    CHATBOT_VECTORIZER_PATH: str = "app/models/chatbot_vectorizer.pkl"
    INTENTS_JSON_PATH: str = "app/models/intents.json"
    FACE_MODEL_PATH: str = "app/models/face_recognition.pkl"
    PRODUCT_MODEL_PATH: str = "app/models/product_classifier.h5"
    SENTIMENT_MODEL_PATH: str = "app/models/sentiment_model.pkl"
    SENTIMENT_VECTORIZER_PATH: str = "app/models/vectorizer.pkl"

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
