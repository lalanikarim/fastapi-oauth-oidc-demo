"""Configuration management for the FastAPI OAuth application."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # FastAPI Configuration
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # OAuth Configuration
    oauth_client_id: str = os.getenv("OAUTH_CLIENT_ID", "demo-client-id")
    oauth_client_secret: str = os.getenv("OAUTH_CLIENT_SECRET", "demo-client-secret")
    oauth_redirect_uri: str = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:8000/auth")
    oauth_scopes: str = os.getenv("OAUTH_SCOPES", "openid offline_access")
    
    # OAuth Provider URLs
    oauth_authorize_url: str = os.getenv("OAUTH_AUTHORIZE_URL", "https://example.com/oauth2/auth")
    oauth_token_url: str = os.getenv("OAUTH_TOKEN_URL", "https://example.com/oauth2/token")
    oauth_userinfo_url: str = os.getenv("OAUTH_USERINFO_URL", "https://example.com/userinfo")
    oauth_jwks_url: str = os.getenv("OAUTH_JWKS_URL", "https://example.com/.well-known/jwks.json")
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    def validate(self) -> None:
        """Validate that required configuration is present."""
        if not self.oauth_client_id or self.oauth_client_id == "demo-client-id":
            raise ValueError(
                "OAUTH_CLIENT_ID environment variable is required. "
                "Please set up your OAuth credentials in a .env file. "
                "See README.md for setup instructions."
            )
        if not self.oauth_client_secret or self.oauth_client_secret == "demo-client-secret":
            raise ValueError(
                "OAUTH_CLIENT_SECRET environment variable is required. "
                "Please set up your OAuth credentials in a .env file. "
                "See README.md for setup instructions."
            )


# Global settings instance
settings = Settings()
