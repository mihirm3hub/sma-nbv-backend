from pydantic import BaseModel
from typing import List

class ObjectPose(BaseModel):
    x: float
    y: float
    z: float

class NBVPoint(BaseModel):
    x: float
    y: float
    z: float
    azimuth: float
    elevation: float

class NBVResponse(BaseModel):
    nbv_points: List[NBVPoint]
