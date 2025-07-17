'''파일 설명을 읽어오는 모듈 - 수정된 버전'''


def leading_multiline_comments(file_path: str) -> str:
    """소스 코드 파일의 맨 첫 줄부터 시작하는 여러 줄 주석을 읽어와 주석 마크를 제거하고 내부 문자열만 반환합니다.

    Args:
        file_path (str): 소스 코드 파일의 경로입니다.

    Returns:
        str: 주석 마크가 제거된 주석 내용입니다.
             파일 시작 부분에 주석이 없거나 파일이 비어있으면 빈 문자열을 반환합니다.
             파일을 찾을 수 없는 경우 오류 메시지를 반환할 수 있습니다.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return ""
    except Exception:
        return ""
    if not lines:
        return ""

    # 1. Python 스타일 주석 ('''...''' 또는 """...""") 확인
    first_line_stripped = lines[0].strip()
    py_multi_delimiters = ['"""', "'''"]
    py_delimiter_used = None

    for delim in py_multi_delimiters:
        if first_line_stripped.startswith(delim):
            py_delimiter_used = delim
            break

    if py_delimiter_used:
        comment_buffer = []
        # 첫 줄에서 주석이 시작하고 끝나는 경우
        if first_line_stripped.endswith(py_delimiter_used) and len(first_line_stripped) >= 2 * len(py_delimiter_used):
            # 같은 구분자가 두 번 나타나는지 확인
            content = first_line_stripped[len(py_delimiter_used):]
            end_pos = content.find(py_delimiter_used)
            if end_pos != -1:
                return content[:end_pos].strip()

        # 여러 줄에 걸친 경우
        # 첫 줄의 내용 (여는 구분자 이후)
        comment_buffer.append(first_line_stripped[len(py_delimiter_used):])

        for i in range(1, len(lines)):
            line_content = lines[i].rstrip('\n')  # 줄 끝 개행 문자만 제거
            closing_delimiter_pos = line_content.find(py_delimiter_used)
            if closing_delimiter_pos != -1:
                comment_buffer.append(line_content[:closing_delimiter_pos])
                return "\n".join(comment_buffer).strip()
            else:
                comment_buffer.append(line_content)
        return ""  # 닫는 구분자를 찾지 못한 경우 (잘못된 형식)

    # 2. C 스타일 블록 주석 (/* ... */) 확인
    first_line_original = lines[0].rstrip('\n')  # 원본 첫 줄 (공백 중요)

    if first_line_original.lstrip().startswith('/*'):
        c_style_comment_parts = []
        start_marker_pos = first_line_original.find('/*')
        content_after_open_marker = first_line_original[start_marker_pos + 2:]

        end_marker_pos_first_line = content_after_open_marker.find('*/')
        if end_marker_pos_first_line != -1:  # 첫 줄에서 시작하고 끝나는 경우
            return content_after_open_marker[:end_marker_pos_first_line].strip()

        c_style_comment_parts.append(
            content_after_open_marker)  # 첫 줄의 /* 이후 내용 추가

        for i in range(1, len(lines)):
            current_line_content = lines[i].rstrip('\n')
            end_marker_pos_current_line = current_line_content.find('*/')
            if end_marker_pos_current_line != -1:  # 닫는 '*/'를 찾은 경우
                c_style_comment_parts.append(
                    current_line_content[:end_marker_pos_current_line])

                # C 스타일 주석 내용 정리 (앞부분의 '*' 등 제거)
                raw_block_text = "\n".join(c_style_comment_parts)
                lines_of_raw_block = raw_block_text.split('\n')

                cleaned_c_style_lines = []
                if lines_of_raw_block:
                    # 주석 블록의 첫 줄 내용
                    first_cleaned = lines_of_raw_block[0].strip()
                    if first_cleaned:
                        cleaned_c_style_lines.append(first_cleaned)

                    # 주석 블록의 중간 줄들 내용 정리
                    for k in range(1, len(lines_of_raw_block)):
                        line = lines_of_raw_block[k]
                        stripped_for_star_check = line.lstrip()
                        if stripped_for_star_check.startswith('*'):
                            content_after_star = stripped_for_star_check[1:]
                            if content_after_star.startswith(' '):  # "* " 패턴
                                cleaned_c_style_lines.append(
                                    content_after_star[1:].rstrip())
                            else:  # "*content" 또는 "*" 패턴
                                cleaned_c_style_lines.append(
                                    content_after_star.rstrip())
                        else:
                            # '*'로 시작하지 않으면 원본 유지 (오른쪽 공백만 제거)
                            cleaned_c_style_lines.append(line.rstrip())

                return "\n".join(cleaned_c_style_lines).strip()
            else:
                c_style_comment_parts.append(current_line_content)
        return ""  # 닫는 '*/'를 찾지 못한 경우 (잘못된 형식)

    # 3. 연속된 한 줄 주석 (#, //, --) 확인
    single_line_markers = ["#", "//", "--"]
    detected_marker = None

    first_line_lstripped = lines[0].lstrip()  # 첫 줄의 왼쪽 공백 제거 후 확인
    for marker_candidate in single_line_markers:
        if first_line_lstripped.startswith(marker_candidate):
            detected_marker = marker_candidate
            break

    if detected_marker:
        comment_lines = []
        for line_idx in range(len(lines)):
            current_line_lstripped = lines[line_idx].lstrip()
            if current_line_lstripped.startswith(detected_marker):
                # 마커 이후의 내용 추출 및 양쪽 공백 제거
                content = current_line_lstripped[len(detected_marker):].strip()
                comment_lines.append(content)
            else:
                # 연속된 주석이 끊긴 경우
                break

        return "\n".join(comment_lines).strip()

    return ""  # 어떤 주석 형식에도 해당하지 않는 경우
