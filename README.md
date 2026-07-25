# limited-edition-demand-forecasting-service

FastAPI service that forecasts resale demand (`totalItemsSold`) for a genuinely new
sneaker release, per US region, using an XGBoost Tweedie regression model.

## Setup

Requires Python >=3.14 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env   # then set a real API_KEY
```

## Running

```bash
uv run main.py
# or
uv run uvicorn app.main:app --reload
```

Server starts on `http://localhost:8000`. Interactive docs at `/docs`.

## Configuration

Settings are read from environment variables / `.env` (see `app/core/config.py`):

| Variable | Default | Description |
|---|---|---|
| `API_KEY` | *(required)* | Key clients must send in the `X-API-Key` header |
| `MODEL_PATH` | `artifacts/v1/xgb_tweedie_new_sku.joblib` | Path to the trained model artifact |
| `HISTORICAL_DEMAND_PATH` | `artifacts/v1/brand_historical_region_demand.json` | Path to the (brand, region) historical demand lookup |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_FILE` | `logs/app.log` | Log file path (rotated at 5MB, 3 backups) |

## API

All routes are versioned under `/api/v1`.

### `GET /api/v1/health`

Unauthenticated liveness check.

```json
{"status": "ok"}
```

### `POST /api/v1/forecast`

Requires an `X-API-Key` header. Returns predicted units sold per region.

Request:

```json
{
  "buyerRegions": ["California", "Texas"],
  "brand": "Yeezy",
  "retailPrice": 220,
  "releaseDate": "2026-11-15",
  "silhouette": "Yeezy-Boost",
  "colorwayType": "named/nickname"
}
```

Response:

```json
{
  "California": 513.62,
  "Texas": 301.63
}
```

`releasedOnWeekend`, `releaseMonth`, and `historicalBrandRegionDemand` are derived
server-side from `releaseDate` and the historical demand lookup — not part of the
request. `brand`, `silhouette`, and `colorwayType` are restricted to the values the
model was trained on (see `app/models/request.py`).

## Model

See `artifacts/v1/xgb_tweedie_new_sku_metadata.json` for training details, features,
and evaluation metrics. The model predicts on a genuine cold-start task — a sneaker
the model has never seen before — using brand, price, silhouette, colorway type, and
historical brand/region demand instead of product identity.

## Project structure

See [project_structure.md](project_structure.md).
