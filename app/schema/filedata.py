"""FileData 선언"""
from enum import Enum
from pydantic import BaseModel


class FileType(str, Enum):
    """파일 타입
    파일이 실행 파일인지, 프로젝트 파일인지, 소스코드인지 타입으로 분류하는 enum 클래스.
    """
    EXECUTION = "실행파일"
    CONF = "환경파일"
    DB = "DB파일"
    PROJECT = "프로젝트 파일"
    SOURCE = "소스코드"
    IMAGE = "이미지 파일"
    UNKNOWN = "미식별 파일"
    ETC = "기타 파일"


class FileData(BaseModel):
    """파일 데이터
    파일 정보를 구성하는 클래스
    """
    device: str
    csu: str
    type: FileType

    index: int
    filePath: str
    filename: str
    version: str
    size: int
    checksum: str
    date: str         # 실행파일 종류는 update date, 소스코드는 create date

    partNumber: str   # 실행파일 목록만
    loc: str          # 소스코드 만, 이미지일 경우 해상도

    description: str  # 가능한 경우.


