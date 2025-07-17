"""entrypoint"""
import os
import shutil
import anyio

from fastapi import BackgroundTasks, Body, FastAPI, File, HTTPException, UploadFile, Form
from app.environments.env import DEFAULT_TEMP_DIR
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.responses import FileResponse, HTMLResponse

from app.schema.enums import CHECKSUM
from app.util import extract_zip, create_random_named_folder
from app.parser import parser
from app.schema.web_api import SpsProject, SpsRequest
from app.parser import project_yaml_parser
from app.hwpx import make_sps_hwpx
from app.util.util import create_template_zip

api = FastAPI()
api.mount("/static", StaticFiles(directory="resources"), name="static")


def get(a, default=None):
    return a if a is not None else default

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


@api.post("/uploadfile/hwpx")
async def upload_file_hwpx(
    file: UploadFile = File(...),
    device: str = Form(...),
    csu: str = Form(...),
    version: str = Form(...),
    partnumber: str = Form(...),
    checksum_type: CHECKSUM = Form(...)
) -> FileResponse:
    if file.filename is None:
        return FileResponse(path="", filename="default_filename")

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
    if os.path.exists(directory_path + "/project.yaml"):
        project_filename = directory_path + "/project.yaml"
    elif os.path.exists(directory_path + "/project.yml"):
        project_filename = directory_path + "/project.yml"
    else:
        project_filename = None

    if project_filename:
        sps_project: SpsProject = project_yaml_parser.parse_sps_project(project_filename)
        retval = parser.get_sps_data_csc(sps_project, directory_path)
    else:
        device_request = SpsRequest(
            device=get(device, "HDEV"),
            csu=get(csu, "CSU"),
            version=get(version, "1.0"),
            partnumber=get(partnumber, "P"),
            checksum_type=get(checksum_type, CHECKSUM.MD5)
        )
        retval = parser.get_sps_data(device_request, directory_path)

    make_sps_hwpx.make(retval, target)
    create_template_zip(target, save_as_location)

    background_tasks = BackgroundTasks()
    background_tasks.add_task(_delete_file, target)

    return FileResponse(path=f"{target}/{save_as_location}",
                        media_type="application/octet-stream",  # 또는 적절한 MIME 타입
                        filename=f"{save_as_location}",
                        headers={
                            "Content-Disposition": f"attachment; filename={save_as_location}"},
                        background=background_tasks)


def _delete_file(path: str) -> None:
    shutil.rmtree(path)
    print(f"'{path}' 디렉토리가 성공적으로 삭제되었습니다.")
