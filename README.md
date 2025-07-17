# make-sps

## 프로젝트 명

make-sps

## 프로젝트에 대한 개략적인 설명

`make-sps`는 소스코드(프로젝트)를 입력하면 자동으로 SPS 파일을 작성해주는 웹 애플리케이션 입니다.  
FastAPI와 Uvicorn을 사용하여 구축되었으며, 다양한 파일 유형에서 메타데이터를 추출하고 hwpx의 XML 문서를 작성합니다.  
이 파일을 hwpx 파일로 변환하여 다운로드하도록 합니다.  
web ui는 cline과 devstral:24b를 이용해 구현했습니다.  
loc counting 및 몇몇 로직은 claude sonnet을 이용해 구현했습니다.  
기본 코드는 C#/Winform/ANTRL4를 이용해 구현했던 기존 버전의 코드를 python으로 재구현한 것을 사용했습니다. 서버에서 구동 가능한 서비스를 만들고 싶어서 재구현했습니다.

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

## 프로젝트 구조

```
.
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
├── run.py
├── uv.lock
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── environments/
│   │   ├── __init__.py
│   │   └── env.py
│   ├── hwpx/
│   │   ├── __init__.py
│   │   ├── hwpx.py
│   │   └── make_sps_hwpx.py
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── code_counter.py
│   │   ├── get_file_description.py
│   │   ├── image_details.py
│   │   ├── parser.py
│   │   └── project_yaml_parser.py
│   ├── schema/
│   │   ├── constants.py
│   │   ├── enums.py
│   │   ├── filedata.py
│   │   └── web_api.py
│   └── util/
│       ├── __init__.py
│       ├── ollama.py
│       └── util.py
├── resources/
│   ├── gui.html
│   ├── index.html
│   ├── scripts.js
│   ├── section0.xml
│   ├── styles.css
│   └── template/
│       ├── mimetype
│       ├── settings.xml
│       ├── version.xml
│       ├── Contents/
│       │   ├── content.hpf
│       │   └── header.xml
│       ├── META-INF/
│       │   ├── container.rdf
│       │   ├── container.xml
│       │   └── manifest.xml
│       └── Preview/
│           ├── PrvImage.png
│           └── PrvText.txt
└── test/
    ├── project.yaml
    ├── test_leading_multiline_comments.py
    └── test_loc.py
```

## 주요 파일 설명

- `app/app.py`: FastAPI 애플리케이션의 엔트리포인트, API 경로 정의
- `app/parser/parser.py`: 다양한 파일 형식에서 메타데이터 추출 및 SPS 데이터 생성
- `run.py`: Uvicorn 서버를 통해 애플리케이션 실행
- `resources/gui.html`: 웹 인터페이스 HTML 파일
- `resources/template/`: HWPX 파일 템플릿 디렉토리

## 기능 설명

1. **파일 업로드 및 처리**:
   - 사용자는 소스코드 프로젝트 파일을 zip 또는 hwpx 형식으로 업로드할 수 있습니다.
   - 서버는 업로드된 파일을 추출하고 각 파일에 대한 메타데이터를 추출합니다.

2. **메타데이터 추출**:
   - 파일 유형에 따라 다른 메타데이터를 추출합니다:
     - 소스 코드: 코드 라인 수
     - 이미지: 크기, 비트 깊이
     - 기타 설정 파일: 관련 정보

3. **SPS 파일 생성**:
   - 추출된 메타데이터를 바탕으로 SPS XML 문서를 생성하고 hwpx 파일로 변환합니다.
   - 사용자에게 다운로드 링크를 제공합니다.

4. **프로젝트 관리**:
   - 프로젝트별 CSU(Component Software Unit) 정보를 관리할 수 있습니다.
   - YAML 형식의 프로젝트 파일을 통해 프로젝트 구조를 정의할 수 있습니다.

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

### ollama 설정

pyproject.toml에 ollama 부분에서 api base와 model을 설정할 수 있습니다.  
파일 설명 부분을 ollama의 모델 부분에 질의하여 가져오도록 구현되어 있습니다.  

## 사용 방법

구현한 프로젝트를 장비별(device)로 한 폴더에 저장하세요.  
CSU 별로 별도 폴더로 저장하세요.  
project.yaml 파일을 장비별 폴더마다 하나씩 작성합니다.  

 - csu : CSU가 들어갈 부분에 작성될 str
 - dir : 해당 CSU의 소스코드 파일이 저장된 폴더

예시

```yaml
project:
  device: HDEV-001
  version: 1.0.0
  partnumber: Q2350911516
  checksum_type: SHA256
  csu:
    - csu: Test1 (D-AAA-SFR-001)
      dir: test1
    - csu: Test2 (D-AAA-SFR-002)
      dir: test2
    - csu: Test3 (D-AAA-SFR-003)
      dir: test3
    - csu: Test4 (D-AAA-SFR-004)
      dir: test4
```

Device 별로 zip으로 압축해주세요.  
UI에서 파일을 업로드하시면 됩니다.  

UI에서 입력하는 각 정보(장비식별자, CSU 등)은 디버그 및 예비용입니다.  

## 라이선스

이 프로젝트는 Apache License 2.0 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.
