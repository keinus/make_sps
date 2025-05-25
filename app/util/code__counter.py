"""LOC 측정 모듈"""
import re


def count_code_lines(filepath) -> int:
    """주어진 파일에서 코드 라인의 수를 세는 함수입니다.
    이 함수는 파일을 열고, 각 줄을 분석하여 코드 라인, 한 줄 주석, 여러 줄 주석을 구분합니다.
    코드 라인은 실질적으로 실행되는 소스 코드 라인을 의미하며, 주석과 빈 줄은 제외됩니다.
    파일 처리 및 오류 처리:
        - 파일 열기 시 FileNotFoundError 또는 기타 예외가 발생하면,
          적절한 오류 메시지를 출력하고 -1을 반환합니다.
        - 파일을 성공적으로 열면, 각 줄을 읽어와서 분석합니다.

    코드 라인 카운트 로직:
        - 빈 줄은 건너뜁니다.
        - 여러 줄 주석 처리: 다중 주석의 시작과 끝을 추적하며, 여러 줄에 걸친 주석도 처리합니다.
          - 주석 내부의 라인은 무시됩니다.
          - 같은 줄에서 시작하고 끝나는 여러 줄 주석도 처리합니다. (예: /* comment */)
        - 한 줄 주석 처리: 특정 패턴으로 시작하는 줄은 주석으로 간주하고, 해당 줄을 건너뜁니다.

    각 줄에 대해:
        - 주석 이전에 코드가 있으면 해당 라인을 코드 라인으로 간주합니다.
        - 주석만 있는 줄은 무시됩니다.

    최종적으로 세어진 코드 라인 수를 반환합니다. 파일 내의 주석 및 빈 줄은 제외됩니다.

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
    multiline_comment_starts = [r'/\*', r'"""', r"'''"]
    multiline_comment_ends = {
        r'/\*': r'\*/',
        r'"""': r'"""',
        r"'''": r"'''"
    }
    current_multiline_start_pattern = None
    single_line_comment_patterns = [r'//', r'#']

    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:
            continue

        # 2. 여러 줄 주석 처리
        if in_multiline_comment:
            # 여러 줄 주석이 끝나는지 확인
            if current_multiline_start_pattern and \
                    _end_match(multiline_comment_ends,
                               current_multiline_start_pattern,
                               stripped_line):
                # 주석 종료 패턴 이후에 코드가 있는지 확인
                # 예: */ int a = 0;
                # 주의: 이 부분은 복잡한 경우 (예: 주석 종료와 시작이 한 줄에 있거나, 코드 중간에 주석 종료)를
                # 완벽하게 처리하지 못할 수 있습니다. 더 정교한 파서가 필요할 수 있습니다.
                end_match = _end_match(multiline_comment_ends,
                                       current_multiline_start_pattern,
                                       stripped_line)
                if end_match:
                    # 주석 종료 이후의 나머지 부분을 다시 검사
                    remaining_line_after_multiline_end = \
                        stripped_line[end_match.end():].strip()
                    if remaining_line_after_multiline_end:
                        # 한 줄 주석이 또 있는지 확인
                        is_single_line_comment_after_multi = False
                        for sl_pattern in single_line_comment_patterns:
                            if remaining_line_after_multiline_end.startswith(
                                    sl_pattern):
                                is_single_line_comment_after_multi = True
                                break
                        if not is_single_line_comment_after_multi:
                            code_lines_count += 1  # 주석 종료 후 코드가 있으면 카운트
                    in_multiline_comment = False
                    current_multiline_start_pattern = None
            # 여러 줄 주석 내부의 라인이면 계속 건너뛰기
            continue

        # 3. 여러 줄 주석 시작 확인
        starts_new_multiline = False
        for ml_start_pattern in multiline_comment_starts:
            if stripped_line.startswith(ml_start_pattern):
                in_multiline_comment = True
                current_multiline_start_pattern = ml_start_pattern
                starts_new_multiline = True
                # 여러 줄 주석이 같은 줄에서 끝나는지 확인 (예: /* comment */)
                # 그리고 주석 이전에 코드가 있는지 확인 (예: int a = 0; /* comment */)
                end_pattern = multiline_comment_ends[ml_start_pattern]
                start_match = re.search(
                    re.escape(ml_start_pattern), stripped_line)
                end_match = re.search(re.escape(end_pattern), stripped_line)

                # 코드와 함께 시작하고 같은 줄에서 끝나는 여러 줄 주석 (예: code /* comment */)
                # 또는 코드 없이 시작하고 같은 줄에서 끝나는 여러 줄 주석 (예: /* comment */)
                if start_match and end_match and\
                        start_match.start() < end_match.start():
                    # 주석 시작 전 코드가 있는지 확인
                    code_before_multiline = \
                        stripped_line[:start_match.start()].strip()
                    if code_before_multiline:
                        code_lines_count += 1

                    # 주석 종료 후 코드가 있는지 확인
                    code_after_multiline = \
                        stripped_line[end_match.end():].strip()
                    if code_after_multiline:
                        # 남은 부분에 한 줄 주석이 있는지 다시 확인
                        is_sl_comment_after_ml = False
                        for sl_pattern_in in single_line_comment_patterns:
                            if code_after_multiline.startswith(sl_pattern_in):
                                is_sl_comment_after_ml = True
                                break
                        if not is_sl_comment_after_ml:
                            code_lines_count += 1
                    in_multiline_comment = False  # 같은 줄에서 끝났으므로 상태 초기화
                    current_multiline_start_pattern = None
                # 여러 줄 주석이 시작되었고, 같은 줄에서 끝나지 않으면 다음 라인부터 주석으로 처리
                elif start_match:
                    code_before_multiline_start =\
                        stripped_line[:start_match.start()].strip()
                    if code_before_multiline_start:
                        code_lines_count += 1
                    # 이 라인의 나머지 부분은 주석이므로 다음 라인으로 넘어감

        # 여러줄 주석으로 시작했고, 아직 주석 상태면 continue
        if starts_new_multiline and in_multiline_comment:
            continue

        # 4. 한 줄 주석 처리
        is_single_line_comment = False
        for sl_pattern in single_line_comment_patterns:
            sl_match = re.search(re.escape(sl_pattern), stripped_line)
            if sl_match:
                # 주석 마커 이전에 코드가 있는지 확인 (예: int a = 0; // comment)
                code_before_comment = stripped_line[:sl_match.start()].strip()
                if code_before_comment:
                    code_lines_count += 1
                is_single_line_comment = True
                break
        if is_single_line_comment:
            continue

        # 5. 위 모든 조건에 해당하지 않으면 코드 라인으로 간주
        code_lines_count += 1

    return code_lines_count


def _end_match(multiline_comment_ends,
               current_multiline_start_pattern,
               stripped_line):
    """주어진 라인에서 다중줄 주석의 종료 패턴을 검색합니다.

    이 함수는 주어진 라인에 특정 다중줄 주석이 끝나는지 여부를 확인하기 위해 사용됩니다.
    이를 통해 코드에서 다중줄 주석의 경계를 명확히 할 수 있습니다.

    Args:
        multiline_comment_ends (dict): 다중줄 주석의 종료 패턴을 저장한 딕셔너리입니다.
                                       각 키는 다중줄 주석의 시작 패턴이고,
                                       값은 해당 주석의 종료 패턴입니다.
        current_multiline_start_pattern (str): 현재 검사 중인 다중줄 주석의 시작 패턴입니다.
        stripped_line (str): 주석을 검사할 대상 라인으로, 앞뒤 공백이 제거된 상태입니다.

    Returns:
        re.Match: 종료 패턴을 찾으면 해당 매치 객체를 반환합니다. 그렇지 않으면 None을 반환합니다.
    """
    return re.search(re.escape(
        multiline_comment_ends[current_multiline_start_pattern]),
        stripped_line)
