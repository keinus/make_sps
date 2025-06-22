"""기본 file parser"""
import datetime
import os
from pathlib import Path
from typing import List
from app.environments.env import DEFAULT_TEMP_DIR
from app.schema.enums import CHECKSUM
from app.schema.filedata import FileType, FileData
from app.schema.constants import (EXECUTION_EXTENSIONS, PROJECT_EXTENSIONS,
                                  SOURCE_EXTENSIONS, CONFIGURATION_EXTENSIONS,
                                  DATABSE_EXTENSIONS, IMAGE_EXTENSIONS)
from app.schema.web_api import SpsRequest
from app.util import get_md5_checksum, get_sha256_checksum
from app.parser.code__counter import count_code_lines
from app.parser.image_details import get_image_details
from app.parser.get_file_description import leading_multiline_comments


def _get_file_type(extension: str) -> FileType:
    """파일의 종류를 리턴
    파일 확장자에 따라 FileType을 반환합니다.

    Args:
        extension (str): 파일 확장자

    Returns:
        FileType: 분류된 파일 타입 (EXECUTION, PROJECT, SOURCE, UNKNOWN).
    """
    if extension in EXECUTION_EXTENSIONS:
        return FileType.EXECUTION
    elif extension in PROJECT_EXTENSIONS:
        return FileType.PROJECT
    elif extension in SOURCE_EXTENSIONS:
        return FileType.SOURCE
    elif extension in CONFIGURATION_EXTENSIONS:
        return FileType.CONF
    elif extension in DATABSE_EXTENSIONS:
        return FileType.DB
    elif extension in IMAGE_EXTENSIONS:
        return FileType.IMAGE
    else:
        return FileType.CONF


def _get_checksum(file_path: str, checksum_type: CHECKSUM) -> str:
    """체크섬 계산
    주어진 파일 경로와 체크섬 유형을 사용하여 파일의 체크섬을 계산하여 반환합니다.
    지원되는 체크섬 유형은 MD5와 SHA256입니다.

    Args:
        file_path (str): 체크섬을 계산할 파일 경로를 나타내는 문자열.
        checksum_type (CHECKSUM): 체크섬 유형 열거체.
                                  현재 지원하는 유형은 CHECKSUM.MD5와 CHECKSUM.SHA256입니다.

    Returns:
        str: 주어진 체크섬 유형에 따라 계산된 체크섬 값을 문자열로 반환합니다.
             만약 파일 경로가 잘못되었거나, 지정된 체크섬 유형을 지원하지 않는 경우 "Error"를 반환합니다.
    """
    checksum = None
    if checksum_type is CHECKSUM.MD5:
        checksum = get_md5_checksum(file_path)
    elif checksum_type is CHECKSUM.SHA256:
        checksum = get_sha256_checksum(file_path)
    return checksum if checksum is not None else "Error"


def _get_date(file_type: FileType, path: Path) -> str:
    """
    주어진 FileType enum 인스턴스에 따라 생성시간 또는 수정날짜를 반환합니다.
    FileType.EXECUTION, FileType.CONF, FileType.DB인 경우 생성일을 반환하고,
    그 외의 경우에는 수정일을을 반환합니다.

    Args:
        file_type_instance (FileType): FileType enum의 인스턴스.

    Returns:
        int: 분류된 그룹 번호 (1 또는 2).
    """
    if file_type in [FileType.EXECUTION, FileType.CONF, FileType.DB]:
        date = path.stat().st_ctime
    else:
        date = path.stat().st_mtime
    return datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d')


def get_file_data(index: int,
                  device: str,
                  csu: str,
                  version: str,
                  partnumber: str,
                  checksum_type: CHECKSUM,
                  file_path: str) -> FileData | None:
    """지정된 파일 경로에서 파일에 대한 데이터를 수집하고 처리하여 FileData 객체를 반환합니다.
    주어진 파일 경로가 유효한 파일인지 확인합니다. 파일 경로가 유효하지 않거나 파일이 존재하지 않으면 None을 반환합니다.
    파일의 이름, 확장자, 크기를 가져옵니다.
    파일의 유형을 결정하고, 소스 파일일 경우 코드 라인 수를 세어 Loc 필드에 저장합니다.
    이미지 파일일 경우 이미지의 너비, 높이 및 비트 정보를 가져와 Loc 필드에 저장합니다.
    파일에 대한 체크섬을 계산하여 FileData 객체에 포함시킵니다.

    Args:
        index (int): 파일의 인덱스.
        device (str): 파일이 속한 장치의 이름.
        csu (str): CSU(Component Software Unit) 정보.
        version (str): 파일 버전 정보.
        partnumber (str): 파트 넘버.
        checksum_type (CHECKSUM): 체크섬 타입.
        file_path (str): 파일의 경로.

    Returns:
        FileData | None: FileData 객체 또는 파일이 존재하지 않을 경우 None을 반환합니다.


    """
    path: Path = Path(file_path)
    if not path.exists() or not path.is_file():
        return None

    filename = path.stem
    extension = path.suffix
    size = path.stat().st_size

    filetype = _get_file_type(extension)

    date = _get_date(filetype, path)
    checksum = _get_checksum(file_path, checksum_type)
    loc = ''
    if filetype is FileType.SOURCE:
        loc = str(count_code_lines(file_path))
    elif filetype is FileType.IMAGE:
        (width, height), bits = get_image_details(file_path)
        loc = f'{width}x{height} {bits}bits'

    desc = leading_multiline_comments(file_path)
    desc = desc if not desc.startswith("파일 읽기 오류") else ""
    directory_name = os.path.dirname(file_path)

    return FileData(
        Device=device,
        Csu=csu,
        Index=index,
        Type=filetype,
        FilePath=directory_name,
        Filename=filename,
        Version=version,
        Size=size,
        Checksum=checksum,
        Date=date,
        PartNumber=partnumber,
        Loc=loc,
        Description=desc
    )


def get_sps_data(device_request: SpsRequest) -> List[FileData]:
    """주어진 디바이스 요청에 대한 SPS 데이터를 가져오는 함수입니다.
    이 함수는 지정된 디렉토리(DEFAULT_TEMP_DIR)에서 파일을 탐색하고,
    각 파일에 대해 파일 데이터를 추출하여 반환합니다. 파일의 이름은 지정된 형식으로 포맷팅되고,
    파일 데이터는 주어진 디바이스 요청 정보를 기반으로 생성됩니다.

    Args:
        device_request (SpsRequest) : 디바이스 요청 정보를 담고 있는 객체입니다.
    Returns:
        List[FileData] : 파일 데이터의 리스트를 반환합니다.
    """
    retval: List[FileData] = []
    try:
        for root, dirs, files in os.walk(DEFAULT_TEMP_DIR):
            index: int = 1
            prefix = f"E{index:03d}"  # 숫자를 3자리 형식으로 포맷팅
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    data = get_file_data(index,
                                         device_request.device,
                                         device_request.csu,
                                         device_request.version,
                                         device_request.partnumber+prefix,
                                         CHECKSUM.SHA256, filepath)
                    retval.append(data)
                    index += 1
                except Exception as e:
                    print(f"'{filepath}' 파일 파싱 중 오류 발생: {e}")
    except Exception as e:
        print(f"디렉토리 처리 또는 삭제 중 오류 발생: {e}")
    return retval
