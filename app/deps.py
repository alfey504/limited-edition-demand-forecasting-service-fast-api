from functools import lru_cache

import joblib
import xgboost

from app.core.config import settings


@lru_cache
def get_model() -> xgboost.XGBRegressor:
    return joblib.load(settings.model_path)
