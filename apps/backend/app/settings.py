from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings for Study Chat Server.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(default="sqlite:///./data/sqlite.db", alias="DATABASE_URL")

    # Server Configuration
    environment: str = Field(default="development", alias="APP_ENV")
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8082, description="Server port number")
    uvicorn_reload: bool = Field(default=True, description="Enable auto-reload")
    cors_origins: Optional[List[str]] = Field(default=["http://localhost:3002"], description="CORS origins")

    # AWS Bedrock
    aws_region: Optional[str] = Field(default=None, alias="AWS_REGION")
    aws_access_key_id: Optional[str] = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(default=None, alias="AWS_SECRET_ACCESS_KEY")
    aws_session_token: Optional[str] = Field(default=None, alias="AWS_SESSION_TOKEN")
    
    # Strands/Bedrock Model
    strands_model_id: str = Field(default="amazon.nova-lite-v1:0")
    strands_max_tokens: Optional[int] = Field(default=8192)
    strands_default_temperature: float = Field(default=0.7)

    # N-Atlas
    n_atlas_api_base: Optional[str] = Field(default=None, alias="N_ATLAS_API_BASE")
    n_atlas_model_id: str = Field(default="openai/n-atlas")

    # Access Control
    enable_access_control: bool = Field(default=True, alias="ENABLE_ACCESS_CONTROL")
    initial_access_code: Optional[str] = Field(default=None, alias="INITIAL_ACCESS_CODE")
    
    # Firebase
    firebase_service_account_json: Optional[str] = Field(default=None, alias="FIREBASE_SERVICE_ACCOUNT_JSON")
    firebase_credentials_path: Optional[str] = Field(default=None, alias="FIREBASE_CREDENTIALS_PATH")


    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if v is None: return ["*"]
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    @model_validator(mode="after")
    def setup_aws_env(self):
        if self.aws_region: os.environ.setdefault("AWS_REGION", self.aws_region)
        if self.aws_access_key_id: os.environ.setdefault("AWS_ACCESS_KEY_ID", self.aws_access_key_id)
        if self.aws_secret_access_key: os.environ.setdefault("AWS_SECRET_ACCESS_KEY", self.aws_secret_access_key)
        if self.aws_session_token: os.environ.setdefault("AWS_SESSION_TOKEN", self.aws_session_token)
        return self

def get_settings() -> Settings:
    return Settings()
