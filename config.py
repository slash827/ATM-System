import os

class Settings:
    """Application settings and configuration"""
    app_name: str = "ATM System API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Security settings
    allowed_hosts: list = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",")
    
    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

settings = Settings()