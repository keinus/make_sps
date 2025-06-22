from pydantic import BaseModel
from app.schema.enums import CHECKSUM


class SpsRequest(BaseModel):
    device: str
    csu: str
    version: str
    partnumber: str
    checksum_type: CHECKSUM
