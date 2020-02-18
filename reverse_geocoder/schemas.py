from typing import List, Tuple

from pydantic import BaseModel


class GeoJsonGeometry(BaseModel):
    type: str
    coordinates: List[Tuple[float, float]]


class GeocodingProps(BaseModel):
    address: str


class GeoJsonFeature(BaseModel):
    type: str
    geometry: GeoJsonGeometry
    properties: GeocodingProps


class GeoJson(BaseModel):
    type: str
    features: List[GeoJsonFeature]


class Coordinate(BaseModel):
    lat: float
    lon: float

    def to_wkt(self):
        return f"POINT({self.lon} {self.lat})"
