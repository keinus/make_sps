from collections import defaultdict
from typing import Dict, List
from app.hwpx import HWPXMLBuilder
from app.schema.filedata import FileData, FileType


builder = HWPXMLBuilder("./resources/section0.xml")


def _get_exe_list(files: list[FileData]) -> List[List[str]]:
    ret_list = []
    index = 0
    path = ""
    for file in files:
        if path != file.filePath:
            path = file.filePath
            ret_list.append(['저장위치: ' + path])

        index += 1
        data = [
            file.type.value, str(index), file.filename, file.version, str(file.size),
            file.checksum, file.date, file.partNumber + f"E{index:03d}",  # 숫자를 3자리 형식으로 포맷팅
            file.description
        ]
        ret_list.append(data)
    return ret_list


def _get_prj_list(files: list[FileData]) -> List[List[str]]:
    ret_list = []
    index = 0
    path = ""
    for file in files:
        if path != file.filePath:
            path = file.filePath
            ret_list.append(['저장위치: ' + path])

        index += 1
        data = [
            str(index), file.filename, file.version, str(file.size),
            file.checksum, file.date, file.loc, file.description
        ]
        ret_list.append(data)
    return ret_list


def _get_etc_list(files: list[FileData]) -> List[List[str]]:
    ret_list = []
    index = 0
    path = ""
    for file in files:
        if path != file.filePath:
            path = file.filePath
            ret_list.append(['저장위치: ' + path])

        index += 1
        data = [
            str(index), file.filename, file.version, str(file.size),
            file.checksum, file.date, file.description
        ]
        ret_list.append(data)
    return ret_list

def group_by_csu(file_data_list: List[FileData]) -> Dict[str, List[FileData]]:
    grouped = defaultdict(list)
    for item in file_data_list:
        grouped[item.csu].append(item)
    return dict(grouped)

def make(file_data_list: List[FileData], path: str) -> None:
    device = file_data_list[0].device
    
    exe_files = sorted(
        [file for file in file_data_list if file.type in {
            FileType.EXECUTION, FileType.CONF, FileType.DB
        }],
        key=lambda x: x.filePath
    )

    prj_files = sorted(
        [file for file in file_data_list if file.type in {FileType.PROJECT}],
        key=lambda x: x.filePath
    )

    grouped_data = defaultdict(list)
    src_files = {}
    for item in file_data_list:
        if item.type in {FileType.SOURCE, FileType.IMAGE}:
            grouped_data[item.csu].append(item)
    
    for csu in sorted(grouped_data.keys()):  # 키를 정렬하여 순회
        src_files[csu] = _get_prj_list(grouped_data[csu])

    etc_files = sorted(
        [file for file in file_data_list if file.type in {FileType.ETC, FileType.UNKNOWN}],
        key=lambda x: x.filePath
    )

    exe_list = _get_exe_list(exe_files)
    prj_list = _get_prj_list(prj_files)
    etc_list = _get_etc_list(etc_files)

    # 실행 파일 부분
    builder.add_para_number_text("실행파일", level=2)
    builder.add_para_number_text(device, level=3)
    builder.add_text(f"  ○ {device}의 실행파일 총 수 : {len(exe_files)}")
    headers = ["구 분", "순번", "파일명", "버전", "크기 (Byte)", "첵섬", "수정일", "SW부품번호", "기능 설명"]
    sizes = [4481, 3231, 4365, 3254, 4229, 6936, 4456, 5436, 7146]
    builder.add_table(exe_list, headers, sizes, "표", 1, "실행파일 목록")
    builder.add_empty_paragraph()
    builder.add_empty_paragraph()

    builder.add_para_number_text("원시 파일", level=2)
    builder.add_para_number_text(device, level=3)
    builder.add_text(f"  ○ {device}의 원시파일 총 수 : {sum(len(lst) for lst in src_files.values())+len(prj_files)}")
    headers = ["순번", "파일명", "버전", "크기 (Byte)", "첵섬", "생성일자", "라인수", "기능 설명"]
    sizes = [2780, 4555, 2330, 3951, 7018, 3651, 3653, 15372]
    builder.add_table(prj_list, headers, sizes, "표", 1, "프로젝트 파일 목록")
    builder.add_empty_paragraph()
    builder.add_empty_paragraph()

    for csu, src_list in src_files.items():
        builder.add_para_number_text(csu, level=4)
        headers = ["순번", "파일명", "버전", "크기 (Byte)", "첵섬", "생성일자", "라인수", "기능 설명"]
        sizes = [2780, 4555, 2330, 3951, 7018, 3651, 3653, 15372]
        builder.add_table(src_list, headers, sizes, "표", 1, "원본(소스) 파일 목록")
        builder.add_empty_paragraph()
        builder.add_empty_paragraph()

    builder.add_para_number_text("기타 파일", level=2)
    headers = ["순번", "파일명", "버전", "크기 (Byte)", "첵섬", "수정일", "비고"]
    sizes = [4669, 8326, 4669, 4669, 4952, 4669, 8622]
    builder.add_table(etc_list, headers, sizes, "표", 1, "기타 파일 목록")
    builder.add_empty_paragraph()
    builder.add_empty_paragraph()

    builder.add_para_number_text("패키징 요구사항", level=2)
    builder.add_text(" SW 산출물 명세서 3.1항의 “실행파일”과 3.2항의 “원본파일”은 CD에 탑재되어 납품된다.")

    builder.add_empty_paragraph()
    builder.add_empty_paragraph()
    builder.save(f'{path}/section0.xml')
