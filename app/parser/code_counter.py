"""LOC 측정 모듈 - 수정된 버전"""
import re


def count_code_lines(filepath) -> int:
    """주어진 파일에서 코드 라인의 수를 세는 함수입니다.
    이 함수는 파일을 열고, 각 줄을 분석하여 코드 라인, 한 줄 주석, 여러 줄 주석을 구분합니다.
    코드 라인은 실질적으로 실행되는 소스 코드 라인을 의미하며, 주석과 빈 줄은 제외됩니다.
    
    Args:
        filepath (str): 코드 라인을 세고자 하는 파일의 경로.

    Returns:
        int: 파일에서 세어진 코드 라인의 수. 오류가 발생하면 -1을 반환합니다.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다 - {filepath}")
        return -1
    except Exception as e:
        print(f"오류: 파일을 읽는 중 문제가 발생했습니다 - {e}")
        return -1

    code_lines_count = 0
    in_multiline_comment = False
    current_ml_end_pattern = None
    
    # 주석 패턴 정의
    ml_comment_patterns = {
        '/*': '*/',
        '"""': '"""',
        "'''": "'''"
    }
    single_line_comment_patterns = ['//', '#']

    for line in lines:
        stripped_line = line.strip()

        # 빈 줄은 건너뛰기
        if not stripped_line:
            continue

        # 여러 줄 주석 내부에 있는 경우
        if in_multiline_comment:
            # 현재 여러줄 주석의 종료 패턴을 찾기
            end_pos = stripped_line.find(current_ml_end_pattern)
            if end_pos != -1:
                # 주석 종료 후 남은 부분 처리
                remaining = stripped_line[end_pos + len(current_ml_end_pattern):].strip()
                in_multiline_comment = False
                current_ml_end_pattern = None
                
                # 주석 종료 후에 코드가 있는지 확인
                if remaining and not _is_comment_line(remaining, single_line_comment_patterns):
                    code_lines_count += 1
            continue

        # 한줄 주석으로 시작하는지 먼저 확인
        is_single_comment_only = _is_comment_line(stripped_line, single_line_comment_patterns)
        if is_single_comment_only:
            continue

        # 현재 줄에서 여러줄 주석 처리
        has_code = False
        
        # 여러줄 주석 패턴 검사
        ml_found = False
        for start_pattern, end_pattern in ml_comment_patterns.items():
            start_pos = stripped_line.find(start_pattern)
            if start_pos != -1:
                ml_found = True
                
                # 주석 시작 전에 코드가 있는지 확인
                code_before = stripped_line[:start_pos].strip()
                if code_before:
                    has_code = True
                
                # 같은 줄에서 주석이 끝나는지 확인
                end_pos = stripped_line.find(end_pattern, start_pos + len(start_pattern))
                if end_pos != -1:
                    # 주석이 같은 줄에서 끝남
                    code_after = stripped_line[end_pos + len(end_pattern):].strip()
                    if code_after and not _is_comment_line(code_after, single_line_comment_patterns):
                        has_code = True
                else:
                    # 여러줄 주석이 시작되고 같은 줄에서 끝나지 않음
                    in_multiline_comment = True
                    current_ml_end_pattern = end_pattern
                break

        # 여러줄 주석이 발견되지 않았거나, 여러줄 주석 전후에 코드가 있는 경우
        if not ml_found:
            # 한줄 주석이 중간에 있는지 확인
            has_inline_comment = False
            for sl_pattern in single_line_comment_patterns:
                comment_pos = stripped_line.find(sl_pattern)
                if comment_pos > 0:  # 0보다 크면 주석 전에 뭔가 있음
                    has_inline_comment = True
                    code_before_comment = stripped_line[:comment_pos].strip()
                    if code_before_comment:
                        has_code = True
                    break
            
            # 한줄 주석이 없으면 전체가 코드
            if not has_inline_comment:
                has_code = True

        # 코드가 있으면 카운트
        if has_code:
            code_lines_count += 1

    return code_lines_count


def _is_comment_line(line, comment_patterns):
    """주어진 라인이 주석으로 시작하는지 확인합니다."""
    for pattern in comment_patterns:
        if line.startswith(pattern):
            return True
    return False
