"""entrypoint"""
import os
import shutil
from fastapi import FastAPI, File, UploadFile, Form
from app.environments.env import DEFAULT_TEMP_DIR
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.schema.enums import CHECKSUM
from app.util import extract_zip
from app.parser import get_sps_data
from app.schema.web_api import SpsRequest


api = FastAPI()

# Serve static files from the "resources" directory
api.mount("/static", StaticFiles(directory="resources"), name="static")

@api.get("/upload")
async def get_upload_page():
    """HTML 파일 업로드 페이지 제공 함수
    업로드 페이지를 제공하는 API 엔드포인트입니다.

    Returns:
        HTML: 업로드 페이지
    """
    with open("resources/gui.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@api.post("/uploadfile/")
async def upload_file(
    file: UploadFile = File(...),
    device: str = Form(...),
    csu: str = Form(...),
    version: str = Form(...),
    partnumber: str = Form(...),
    checksum_type: CHECKSUM = Form(...)
):
    """파일 업로드 함수
    파일 업로드를 처리하는 API 엔드포인트입니다.
    업로드된 파일을 지정된 디렉토리에 저장하고, 파일의 메타데이터를 반환합니다.

    Args:
        file (UploadFile): 업로드할 파일 객체
        device (str): 장비 식별자
        csu (str): CSU
        version (str): 버전
        partnumber (str): 도면번호(SW부품번호)
        checksum_type (CHECKSUM): 체크섬 타입

    Returns:
        dict: 파일의 이름, 콘텐츠 타입 및 크기를 포함하는 딕셔너리
    """
    if file.filename is not None:
        file_location = f"uploads/{file.filename}"

        os.makedirs(DEFAULT_TEMP_DIR, exist_ok=True)
        os.makedirs("uploads", exist_ok=True)

        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        if file.filename.endswith(".zip"):
            extract_zip(file_location, DEFAULT_TEMP_DIR)
        else:
            target = f"{DEFAULT_TEMP_DIR}/{file.filename}"
            shutil.move(file_location, target)

        # Create SpsRequest from form data
        device_request = SpsRequest(
            device=device,
            csu=csu,
            version=version,
            partnumber=partnumber,
            checksum_type=checksum_type
        )

        retval = get_sps_data(device_request)
        shutil.rmtree(DEFAULT_TEMP_DIR)
        print(f"'{file_location}' 디렉토리가 성공적으로 삭제되었습니다.")

        return retval
    return None
