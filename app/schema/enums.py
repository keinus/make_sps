from enum import Enum


class CHECKSUM(str, Enum):
    """체크섬 타입
    체크섬 타입
    """
    MD5 = "MD5"
    SHA256 = "SHA256"
