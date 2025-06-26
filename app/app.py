"""entrypoint"""
import os
import shutil
import anyio

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile, Form
from app.environments.env import DEFAULT_TEMP_DIR
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.responses import FileResponse, HTMLResponse

from app.schema.enums import CHECKSUM
from app.util import extract_zip, create_random_named_folder
from app.parser import parser
from app.schema.web_api import SpsRequest
# from app.hwp import make_sps_hwp
from app.hwpx import make_sps_hwpx
from app.util.util import create_template_zip

api = FastAPI()
api.mount("/static", StaticFiles(directory="resources"), name="static")


@api.get("/")
async def get_upload_page():
    """HTML 파일 업로드 페이지 제공 함수
    업로드 페이지를 제공하는 API 엔드포인트입니다.

    Returns:
        HTML: 업로드 페이지
    """
    async with await anyio.open_file("resources/gui.html", "r", encoding='UTF8') as file:
        contents = await file.read()
        return HTMLResponse(content=contents, status_code=200)


@api.post("/uploadfile/hwp")
async def upload_file(
    file: UploadFile = File(...),
    device: str = Form(...),
    csu: str = Form(...),
    version: str = Form(...),
    partnumber: str = Form(...),
    checksum_type: CHECKSUM = Form(...)
) -> FileResponse | None:
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
        os.makedirs(DEFAULT_TEMP_DIR, exist_ok=True)
        os.makedirs("uploads", exist_ok=True)

        try:
            target = create_random_named_folder(DEFAULT_TEMP_DIR)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"{e}") from e

        file_location = f"{target}/{file.filename}"
        directory_path = f"{target}/{os.path.splitext(file.filename)[0]}"
        save_as_location = f"{directory_path}.hwp"

        async with await anyio.open_file(file_location, "wb") as buffer:
            await buffer.write(await file.read())

        if file.filename.endswith(".zip"):
            extract_zip(file_location, directory_path)

        # Create SpsRequest from form data
        device_request = SpsRequest(
            device=device,
            csu=csu,
            version=version,
            partnumber=partnumber,
            checksum_type=checksum_type
        )

        retval = parser.get_sps_data(device_request, directory_path)

        result_filename: str = make_sps_hwp.make(retval, save_as_location)

        background_tasks = BackgroundTasks()
        background_tasks.add_task(_delete_file, target)

        return FileResponse(path=result_filename, media_type="application/octet-stream",
                             background=background_tasks)

@api.post("/uploadfile/hwpx")
async def upload_file_hwpx(
    file: UploadFile = File(...),
    device: str = Form(...),
    csu: str = Form(...),
    version: str = Form(...),
    partnumber: str = Form(...),
    checksum_type: CHECKSUM = Form(...)
) -> FileResponse:
    if file.filename is not None:
        os.makedirs(DEFAULT_TEMP_DIR, exist_ok=True)
        os.makedirs("uploads", exist_ok=True)

        try:
            target = create_random_named_folder(DEFAULT_TEMP_DIR)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"{e}") from e

        file_location = f"{target}/{file.filename}"
        directory_path = f"{target}/{os.path.splitext(file.filename)[0]}"
        save_as_location = f"{os.path.splitext(file.filename)[0]}.hwpx"

        async with await anyio.open_file(file_location, "wb") as buffer:
            await buffer.write(await file.read())

        if file.filename.endswith(".zip"):
            extract_zip(file_location, directory_path)

        # Create SpsRequest from form data
        device_request = SpsRequest(
            device=device,
            csu=csu,
            version=version,
            partnumber=partnumber,
            checksum_type=checksum_type
        )

        retval = parser.get_sps_data(device_request, directory_path, target)

        make_sps_hwpx.make(retval, target)
        create_template_zip(target, save_as_location)

        background_tasks = BackgroundTasks()
        background_tasks.add_task(_delete_file, target)

        return FileResponse(path=f"{target}/{save_as_location}",
                            media_type="application/octet-stream",  # 또는 적절한 MIME 타입
                            filename=f"{save_as_location}",
                            headers={"Content-Disposition": f"attachment; filename={save_as_location}"},
                            background=background_tasks)

def _delete_file(path: str) -> None:
    shutil.rmtree(path)
    print(f"'{path}' 디렉토리가 성공적으로 삭제되었습니다.")
