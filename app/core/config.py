from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "limited-edition-demand-forecasting-service"
    model_path: str = "artifacts/v1/xgb_tweedie_new_sku.joblib"
    historical_demand_path: str = "artifacts/v1/brand_historical_region_demand.json"
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    api_key: str


settings = Settings()
