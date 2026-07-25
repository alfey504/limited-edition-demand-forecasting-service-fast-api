import json
from functools import lru_cache

import xgboost

from app.core.config import settings
from app.models.request import ForecastRequest


@lru_cache
def _load_brand_historical_region_demand() -> dict[str, dict[str, float]]:
    with open(settings.historical_demand_path) as f:
        return json.load(f)


def _get_brand_historical_demand(brand: str, region: str) -> float:
    return _load_brand_historical_region_demand()[brand][region]


def forecast(request: ForecastRequest, model: xgboost.XGBRegressor) -> dict[str, float]:
    historical_demand_by_region = {
        region: _get_brand_historical_demand(request.brand.value, region.value)
        for region in request.buyerRegions
    }
    df = request.to_dataframe(historical_demand_by_region)
    predictions = model.predict(df)
    return {
        region.value: float(prediction)
        for region, prediction in zip(request.buyerRegions, predictions)
    }
