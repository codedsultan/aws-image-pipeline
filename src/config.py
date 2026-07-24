from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Runtime configuration for the image-processor Lambda.
    Populated from environment variables set by Terraform - never hardcoded,
    never read via os.environ directly elsewhere in the codebase.
    """

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)

    raw_bucket: str
    processed_bucket: str
    sns_topic_arn: str
    log_level: str = "INFO"
    thumbnail_max_dimension: int = 800


settings = Settings()
