# make-sps

## 프로젝트 명

make-sps

## 프로젝트에 대한 개략적인 설명

`make-sps`는 소스코드(프로젝트)를 입력하면 자동으로 SPS 파일을 작성해주는 웹 애플리케이션 입니다.  
FastAPI와 Uvicorn을 사용하여 구축되었으며, 다양한 파일 유형에서 메타데이터를 추출하고 hwpx의 XML 문서를 작성합니다.  
이 파일을 hwpx 파일로 변환하여 다운로드하도록 합니다.

## 작성자

Byeongjin Kim(bj001.kim@gmail.com)

## 작성 언어

Python 3.10

## 사용 프레임워크

- FastAPI 0.78.0
- Uvicorn 0.17.6

## 사용 라이브러리

- fastapi
- uvicorn
- pyhwpx
- Pillow
- pydantic
- requests

(완전한 목록은 `pyproject.toml` 파일 참고)

## 해당 프로젝트의 빌드 방법

### 사전 준비 사항

- Python 3.10 이상이 설치되어 있어야 합니다.
- uv가 실행되어 있어야 합니다.
  - sudo apt install uv
  - 또는
  - pip install uv

### 빌드 방법

별도 빌드 없음.

### 실행

```bash
uv run run.py
```

이후 웹 브라우저에서 `http://localhost:8000`에 접속하여 애플리케이션을 사용할 수 있습니다.

## 라이선스

이 프로젝트는 Apache License 2.0 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.
