"""utility 모듈"""
import zipfile
import os
import hashlib
import shutil
import uuid


def create_template_zip(target_dir: str, zip_file_name: str) -> None:
    os.makedirs(target_dir, exist_ok=True)
    current_dir = os.path.dirname("./")
    resource_template_src = os.path.join(current_dir, "resources", "template")
    
    target_template_dest = os.path.join(target_dir, "template")
    
    if os.path.exists(target_template_dest):
        shutil.rmtree(target_template_dest)
        print(f"기존 폴더 삭제: {target_template_dest}")
    
    try:
        shutil.copytree(resource_template_src, target_template_dest)
        print(f"'{resource_template_src}' 내용을 '{target_template_dest}'에 복사했습니다.")
    except Exception as e:
        print(f"템플릿 복사 중 오류 발생: {e}")
        return

    section0_xml_src = os.path.join(target_dir, "section0.xml")
    section0_xml_dest_dir = os.path.join(target_template_dest, "Contents")
    section0_xml_dest_file = os.path.join(section0_xml_dest_dir, "section0.xml")

    if not os.path.exists(section0_xml_src):
        print(f"오류: 원본 파일 '{section0_xml_src}'을 찾을 수 없습니다.")
        return

    os.makedirs(section0_xml_dest_dir, exist_ok=True)

    try:
        shutil.copy2(section0_xml_src, section0_xml_dest_file)
        print(f"'{section0_xml_src}'을 '{section0_xml_dest_file}'에 복사했습니다.")
    except Exception as e:
        print(f"section0.xml 복사 중 오류 발생: {e}")
        return
    
    zip_output_path = os.path.join(target_dir, zip_file_name)

    try:
        with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(target_template_dest):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, target_template_dest)
                    zipf.write(file_path, arcname)
        print(f"'{target_template_dest}' 폴더가 '{zip_output_path}'으로 성공적으로 압축되었습니다.")
    except Exception as e:
        print(f"파일 압축 중 오류 발생: {e}")
        return


def extract_zip(zip_path: str, extract_to: str) -> None:
    """zip 파일 압축 해제  
    ZIP 파일을 지정된 경로에 압축 해제합니다.

    :param zip_path: ZIP 파일 경로
    :param extract_to: 압축 해제할 디렉토리 경로
    """
    # 지정된 디렉토리가 없으면 생성
    os.makedirs(extract_to, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def get_md5_checksum(file_path: str, chunk_size: int = 8192) -> str | None:
    """MD5 체크섬 계산 함수  
    파일의 MD5 체크섬을 계산하여 16진수 문자열로 반환합니다.  
    대용량 파일을 효율적으로 처리하기 위해 파일을 청크 단위로 읽습니다.  

    Args:
        file_path (str): MD5 체크섬을 계산할 파일의 경로.
        chunk_size (int): 한 번에 읽을 파일의 청크 크기 (바이트 단위). 기본값은 8192 (8KB).

    Returns:
        str | None: 파일의 MD5 체크섬 16진수 문자열.
                    파일이 존재하지 않거나 읽기 오류 발생 시 None을 반환합니다.
    """
    try:
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_hash.update(chunk)
        return md5_hash.hexdigest()
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다 - {file_path}")
        return None
    except PermissionError:
        print(f"오류: 파일 읽기 권한이 없습니다 - {file_path}")
        return None
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")
        return None


def get_sha256_checksum(file_path: str, chunk_size: int = 8192) -> str | None:
    """SHA256 체크섬 계산 함수
    파일의 SHA256 체크섬을 계산하여 16진수 문자열로 반환합니다.

    대용량 파일을 효율적으로 처리하기 위해 파일을 청크 단위로 읽습니다.

    Args:
        file_path (str): SHA256 체크섬을 계산할 파일의 경로.
        chunk_size (int): 한 번에 읽을 파일의 청크 크기 (바이트 단위). 기본값은 8192 (8KB).

    Returns:
        str | None: 파일의 SHA256 체크섬 16진수 문자열.
                     파일이 존재하지 않거나 읽기 오류 발생 시 None을 반환합니다.
    """
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # 파일의 끝에 도달할 때까지 청크 단위로 읽어서 해시 업데이트
            while chunk := f.read(chunk_size):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다 - {file_path}")
        return None
    except PermissionError:
        print(f"오류: 파일 읽기 권한이 없습니다 - {file_path}")
        return None
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")
        return None


def create_random_named_folder(base_path: str="./temp") -> str:
    """
    주어진 기준 경로에 UUID 기반의 랜덤한 폴더를 생성하고, 생성된 폴더의 전체 경로를 반환하는 함수

    1. UUID 기반의 고유한 폴더명 생성
       - uuid.uuid4()를 사용하여 128비트 고유 식별자 생성
       - 문자열로 변환하여 폴더명으로 사용

    2. 폴더 경로 생성
       - os.path.join()을 통해 기준 경로와 랜덤 폴더명을 결합
       - 예: base_path가 "./temp"일 경우 "/temp/uuid4()" 구조가 됨

    3. 디렉토리 생성 시도
       - os.makedirs()를 사용하여 디렉토리 생성
       - exist_ok=True로 설정하여 기존 디렉토리가 있어도 예외 발생하지 않음

    4. 성공 시
       - 생성된 디렉토리의 전체 경로를 반환

    5. 실패 시
       - OSError 발생 시 원인을 포함한 상세한 에러 메시지 반환
       - 예: "Failed to create directory '/temp/123e4567-e89b-12d3-a456-426614174000': [Errno 17] File exists: '/temp/123e4567-e89b-12d3-a456-426614174000'"

    Parameters:
        base_path (str): 생성할 랜덤 폴더의 기준 경로 (기본값: "./temp")

    Returns:
        str: 생성된 랜덤 폴더의 전체 경로

    Raises:
        OSError: 디렉토리 생성 실패 시 발생
    """
    folder_name = str(uuid.uuid4())
    full_path = os.path.join(base_path, folder_name)

    try:
        os.makedirs(full_path, exist_ok=True)
        return full_path
    except OSError as e:
        raise OSError(f"Failed to create directory '{full_path}': {e}")
