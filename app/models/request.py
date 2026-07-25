from datetime import date
from enum import Enum

import pandas as pd
from pydantic import BaseModel, Field

CATEGORICAL_COLUMNS = ["buyerRegion", "brand", "silhouette", "colorwayType"]


class USRegion(str, Enum):
    ALABAMA = "Alabama"
    ALASKA = "Alaska"
    ARIZONA = "Arizona"
    ARKANSAS = "Arkansas"
    CALIFORNIA = "California"
    COLORADO = "Colorado"
    CONNECTICUT = "Connecticut"
    DELAWARE = "Delaware"
    DISTRICT_OF_COLUMBIA = "District of Columbia"
    FLORIDA = "Florida"
    GEORGIA = "Georgia"
    HAWAII = "Hawaii"
    IDAHO = "Idaho"
    ILLINOIS = "Illinois"
    INDIANA = "Indiana"
    IOWA = "Iowa"
    KANSAS = "Kansas"
    KENTUCKY = "Kentucky"
    LOUISIANA = "Louisiana"
    MAINE = "Maine"
    MARYLAND = "Maryland"
    MASSACHUSETTS = "Massachusetts"
    MICHIGAN = "Michigan"
    MINNESOTA = "Minnesota"
    MISSISSIPPI = "Mississippi"
    MISSOURI = "Missouri"
    MONTANA = "Montana"
    NEBRASKA = "Nebraska"
    NEVADA = "Nevada"
    NEW_HAMPSHIRE = "New Hampshire"
    NEW_JERSEY = "New Jersey"
    NEW_MEXICO = "New Mexico"
    NEW_YORK = "New York"
    NORTH_CAROLINA = "North Carolina"
    NORTH_DAKOTA = "North Dakota"
    OHIO = "Ohio"
    OKLAHOMA = "Oklahoma"
    OREGON = "Oregon"
    PENNSYLVANIA = "Pennsylvania"
    RHODE_ISLAND = "Rhode Island"
    SOUTH_CAROLINA = "South Carolina"
    SOUTH_DAKOTA = "South Dakota"
    TENNESSEE = "Tennessee"
    TEXAS = "Texas"
    UTAH = "Utah"
    VERMONT = "Vermont"
    VIRGINIA = "Virginia"
    WASHINGTON = "Washington"
    WEST_VIRGINIA = "West Virginia"
    WISCONSIN = "Wisconsin"
    WYOMING = "Wyoming"


class Brand(str, Enum):
    YEEZY = "Yeezy"
    OFF_WHITE = "Off-White"


class Silhouette(str, Enum):
    YEEZY_BOOST = "Yeezy-Boost"
    AIR_JORDAN = "Air-Jordan"
    AIR_FORCE = "Air-Force"
    AIR_MAX = "Air-Max"
    AIR_PRESTO = "Air-Presto"
    AIR_VAPORMAX = "Air-VaporMax"
    BLAZER = "Blazer"
    HYPERDUNK = "Hyperdunk"
    ZOOM_FLY = "Zoom-Fly"


class ColorwayType(str, Enum):
    NAMED = "named/nickname"
    DESCRIPTIVE = "descriptive/color-word"
    NONE = "no colorway (base release)"


class ForecastRequest(BaseModel):
    buyerRegions: list[USRegion]
    brand: Brand
    retailPrice: float = Field(gt=0)
    releaseDate: date
    silhouette: Silhouette
    colorwayType: ColorwayType

    def __is_released_on_weekend(self) -> bool:
        return self.releaseDate.weekday() >= 5

    def __get_release_month(self) -> int:
        return self.releaseDate.month

    def to_dataframe(self, historical_demand_by_region: dict[USRegion, float]) -> pd.DataFrame:
        rows = [
            {
                "buyerRegion": region.value,
                "brand": self.brand.value,
                "retailPrice": self.retailPrice,
                "releasedOnWeekend": int(self.__is_released_on_weekend()),
                "releaseMonth": self.__get_release_month(),
                "silhouette": self.silhouette.value,
                "colorwayType": self.colorwayType.value,
                "historicalBrandRegionDemand": historical_demand_by_region[region],
            }
            for region in self.buyerRegions
        ]
        df = pd.DataFrame(rows)
        for col in CATEGORICAL_COLUMNS:
            df[col] = df[col].astype("category")
        return df
