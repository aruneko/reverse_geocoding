from typing import Iterator

from sqlalchemy import func
from sqlalchemy.orm import Session

from reverse_geocoder.models import OoazaPolygon
from reverse_geocoder.schemas import Coordinate


def create_ooaza_polygons(db: Session, polygons: Iterator[OoazaPolygon]):
    db.bulk_save_objects(polygons)
    db.commit()


def find_ooaza(db: Session, coordinate: Coordinate):
    ooaza = (
        db.query(
            OoazaPolygon.prefecture_name,
            OoazaPolygon.city_name,
            OoazaPolygon.ooaza,
            OoazaPolygon.polygon,
        )
        .filter(
            func.ST_Contains(
                OoazaPolygon.polygon, func.ST_GeomFromText(coordinate.to_wkt())
            )
        )
        .first()
    )
    return ooaza
