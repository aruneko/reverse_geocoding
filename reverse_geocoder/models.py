from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String

from .database import Base


class OoazaPolygon(Base):
    __tablename__ = "ooaza_polygon"

    id = Column(Integer, autoincrement=True, primary_key=True)
    prefecture_name = Column(String)
    city_name = Column(String)
    ooaza = Column(String)
    polygon = Column(Geometry("POLYGON"))
