from typing import List, Literal
from app.schema.filedata import FileData, FileType

from pyhwpx import Hwp
from app.hwp.hwpaction import HwpAction

exe_columns = [
    "구 분", "순번", "파일명", "버전",
    "크기 (Byte)", "첵섬", "수정일", "SW부품번호", "기능 설명"
]
exe_columns_width = [
    15.81, 11.40, 15.40, 11.48,
    14.92, 24.47, 15.72, 19.18, 25.21
]

prj_columns = [
    "순번", "파일명", "버전", "크기 (Byte)",
    "첵섬", "생성일자", "라인수", "기능 설명"
]
prj_columns_width = [
    9.81, 16.07, 8.22, 13.94,
    24.76, 12.88, 12.89, 54.23
]

unknown_columns = [
    "순번", "파일명", "버전", "크기 (Byte)",
    "첵섬", "수정일", "비고"
]
unknown_columns_width = [
    16.47, 29.37, 16.47, 16.47,
    24.47, 16.47, 30.42
]


def make(file_data_list: List[FileData], path: str) -> str:
    device = file_data_list[0].Device
    csu = file_data_list[0].Csu
    
    exe_files = sorted(
        [file for file in file_data_list if file.Type in {
            FileType.EXECUTION, FileType.CONF, FileType.DB}],
        key=lambda x: x.FilePath
    )

    prj_files = sorted(
        [file for file in file_data_list if file.Type in {FileType.PROJECT}],
        key=lambda x: x.FilePath
    )

    src_files = sorted(
        [file for file in file_data_list if file.Type in {
            FileType.SOURCE, FileType.IMAGE}],
        key=lambda x: x.FilePath
    )

    unknown_files = sorted(
        [file for file in file_data_list if file.Type in {FileType.UNKNOWN}],
        key=lambda x: x.FilePath
    )

    try:
        hwp = Hwp()
        file_path = "./resources/template.hwp"
        hwp.open(file_path)
    except Exception as e:
        print(f"한/글 프로그램 실행에 실패했습니다: {e}")
        exit()

    action = HwpAction(hwp)

    action.set_para_number_text("실행파일", 2, "02_본문_항목제목")
    action.set_para_number_text(device, 3, "02_본문_항목제목")
    action.set_style_with_text(
        f"  ○ {device}의 실행파일 총 수 : {len(exe_files)}", "03_본문_내용")
    action.BreakPara()

    _create_table(action, exe_files, exe_columns, exe_columns_width)
    _insert_files(action, exe_files, "Exe")
    action.set_caption("실행파일 목록")
    action.BreakPara()
    action.BreakPara()

    action.set_para_number_text("원시 파일", 2, "02_본문_항목제목")
    action.set_style_with_text("CSCI 형상항목 구성", "04_도표그림_제목")
    action.set_para_number_text(device, 3, "02_본문_항목제목")
    action.set_style_with_text(
        f"  ○ {device}의 원시파일 총 수 : {len(src_files)+len(prj_files)}", "03_본문_내용")
    action.BreakPara()

    _create_table(action, prj_files, prj_columns, prj_columns_width)
    _insert_files(action, prj_files, "Prj/Src")
    action.set_caption("프로젝트 파일 목록")
    action.BreakPara()
    action.BreakPara()

    action.set_para_number_text(csu, 4, "02_본문_항목제목")
    _create_table(action, src_files, prj_columns, prj_columns_width)
    _insert_files(action, src_files, "Prj/Src")
    action.set_caption("원본(소스)파일 목록")
    action.BreakPara()
    action.BreakPara()

    if len(unknown_files) > 0:
        action.set_para_number_text("기타 파일", 2, "02_본문_항목제목")
        _create_table(action, unknown_files, unknown_columns, unknown_columns_width)
        _insert_files(action, unknown_files, "Unknown")
        action.set_caption("기타 파일 목록")

    return action.save(path)


def _create_table(action: HwpAction,
                  data_list: List[FileData],
                  columns: List[str],
                  columns_width: List[float]):
    unique_filepaths = set(item.FilePath for item in data_list)
    count_unique_filepaths = len(unique_filepaths)
    low_count = len(data_list) + count_unique_filepaths + 1
    column_count = len(columns)

    action.create_table(rows=low_count, cols=column_count,
                        treat_as_char=False, header=True)
    action.set_table_columns(columns, columns_width)


def _insert_files(action: HwpAction,
                  files: List[FileData],
                  filetype: Literal["Exe", "Prj/Src", "Unknown"]):
    path = ""
    index = 0
    for file in files:
        index += 1
        if path != file.FilePath:
            path = file.FilePath
            action.merge_table_row()
            action.set_column_cel_border(True, True, True, True)
            action.insert_text('저장위치: ' + path)
            action.set_style("07_도표내용_본문혼합")
            action.TableRightCell()
        data = ""
        if filetype == "Exe":
            data = [file.Type.value,
                    str(index),
                    file.Filename,
                    file.Version,
                    str(file.Size),
                    file.Checksum,
                    file.Date,
                    file.PartNumber + f"E{index:03d}",  # 숫자를 3자리 형식으로 포맷팅
                    file.Description]
        elif filetype == "Prj/Src":
            data = [str(index),
                    file.Filename,
                    file.Version,
                    str(file.Size),
                    file.Checksum,
                    file.Date,
                    file.Loc,
                    file.Description]
        elif filetype == "Unknown":
            data = [str(index),
                    file.Filename,
                    file.Version,
                    str(file.Size),
                    file.Checksum,
                    file.Date,
                    file.Description]
        action.set_row(*data)
    action.set_table_border(True, True, True, True)
