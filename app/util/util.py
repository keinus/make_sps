"""utility 모듈"""
import zipfile
import os
import hashlib


def extract_zip(zip_path, extract_to):
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
