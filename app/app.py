"""entrypoint"""
import os
import shutil
from typing import Any

import anyio
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.environments.env import DEFAULT_TEMP_DIR
from app.hwpx import make_sps_hwpx
from app.parser import parser, project_yaml_parser
from app.schema.web_api import SpsProject
from app.util import create_random_named_folder, extract_zip
from app.util.util import create_template_zip

api = FastAPI()
api.mount("/static", StaticFiles(directory="static"), name="static")


def get(a, default=None) -> Any | None:
    return a if a is not None else default

@api.get("/")
async def get_upload_page() -> HTMLResponse:
    """HTML 파일 업로드 페이지 제공 함수
    업로드 페이지를 제공하는 API 엔드포인트입니다.

    Returns:
        HTML: 업로드 페이지
    """
    async with await anyio.open_file("static/index.html", "r", encoding='UTF8') as file:
        contents = await file.read()
        return HTMLResponse(content=contents, status_code=200)


@api.post("/uploadfile")
async def upload_file_hwpx(
    file: UploadFile = File(...),
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
        raise FileNotFoundError("project.yaml not found.")
    

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
