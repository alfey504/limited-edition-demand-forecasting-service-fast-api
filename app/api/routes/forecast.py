import logging
import time

import xgboost
from fastapi import APIRouter, Depends

from app.core.security import verify_api_key
from app.deps import get_model
from app.models.request import ForecastRequest
from app.services.forecaster import forecast as run_forecast

logger = logging.getLogger(__name__)

router = APIRouter(tags=["forecast"], dependencies=[Depends(verify_api_key)])


@router.post("/forecast")
def create_forecast(
    request: ForecastRequest, model: xgboost.XGBRegressor = Depends(get_model)
) -> dict[str, float]:
    logger.info("Forecast requested: brand=%s regions=%d", request.brand, len(request.buyerRegions))
    start = time.perf_counter()
    result = run_forecast(request, model)
    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info("Forecast completed in %.2fms: %s", elapsed_ms, result)
    return result
