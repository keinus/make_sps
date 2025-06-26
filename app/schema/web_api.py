from pydantic import BaseModel
from app.schema.enums import CHECKSUM
from typing import List


class SpsRequest(BaseModel):
    """단일 프로젝트 요청"""
    device: str
    csu: str
    version: str
    partnumber: str
    checksum_type: CHECKSUM


class Csu(BaseModel):
    """CSU 스키마"""
    csu: str
    dir: str


class SpsProject(BaseModel):
    """프로젝트 스키마"""
    device: str
    version: str
    partnumber: str
    checksum_type: str
    csu: List[Csu]
