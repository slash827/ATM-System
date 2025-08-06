"""
Core application configuration and settings
"""
import os
from typing import List

class Settings:
    """Application settings and configuration"""
    app_name: str = "ATM System API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Security settings
    allowed_hosts: List[str] = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",")
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./atm_system.db")
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    
    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

# Global settings instance
settings = Settings()
