from argparse import ArgumentParser
from pathlib import Path
from typing import Tuple, List

import shapefile

from reverse_geocoder.crud import create_ooaza_polygons
from reverse_geocoder.database import SessionLocal, engine, Base
from reverse_geocoder.models import OoazaPolygon


Base.metadata.create_all(bind=engine)
session = SessionLocal()


def to_wkt_polygon(points: List[Tuple[float, float]]) -> str:
    return (
        "POLYGON(("
        + ", ".join(map(lambda point: f"{point[0]} {point[1]}", points))
        + f", {points[0][0]} {points[0][1]}))"
    )


def to_alchemy(shape: shapefile.ShapeRecord) -> OoazaPolygon:
    polygon_points = shape.shape.points
    wkt_polygon = to_wkt_polygon(polygon_points)

    record = shape.record
    prefecture: str = record[4]
    city: str = record[16]
    ward: str = record[5]
    ooaza = record[6]

    return OoazaPolygon(
        prefecture_name=prefecture,
        city_name=city + ward if ward.endswith("区") else city,
        ooaza=ooaza,
        polygon=wkt_polygon,
    )


def save_ooaza_polygon(shape_file: shapefile.Reader):
    record_shapes = shape_file.shapeRecords()
    rows = map(lambda shape: to_alchemy(shape), record_shapes)
    create_ooaza_polygons(session, list(rows))


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("polygon_shp_path")
    args = parser.parse_args()

    shape_file_path = Path(args.polygon_shp_path)
    shape_files = shape_file_path.glob("**/*.shp")

    for shape_file in shape_files:
        save_ooaza_polygon(shapefile.Reader(str(shape_file), encoding="cp932"))


if __name__ == "__main__":
    main()
