from fastapi import FastAPI, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from reverse_geocoder.crud import find_ooaza
from reverse_geocoder.database import SessionLocal
from reverse_geocoder.schemas import (
    Coordinate,
    GeoJson,
    GeoJsonFeature,
    GeocodingProps,
    GeoJsonGeometry,
)

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def aliveness():
    return {"status": "alive"}


@app.post("/reverse_geocode")
async def reverse_geocode(coordinate: Coordinate, db: Session = Depends(get_db)):
    ooaza = find_ooaza(db, coordinate)
    # Get polygon data as a string
    polygon_text: str = db.scalar(func.ST_AsText(ooaza[3]))
    # "POLYGON((x y, x y, ...))" -> ["x y", "x y", ...]
    polygon_text_list = polygon_text.replace('POLYGON', '')[2:-2].split(',')
    # ["x y", "x y", ...] -> [[x, y], [x, y], ...]
    polygon = map(lambda t: list(map(lambda p: float(p), t.split(' '))), polygon_text_list)
    response = GeoJson(
        type="FeatureCollection",
        features=[
            GeoJsonFeature(
                type="Feature",
                geometry=GeoJsonGeometry(type="LineString", coordinates=list(polygon)),
                properties=GeocodingProps(address=f"{ooaza[0]}{ooaza[1]}{ooaza[2]}"),
            )
        ],
    )
    return response
