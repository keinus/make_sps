import xml.etree.ElementTree as ET
from typing import List


class HWPXMLBuilder:
    """HWP XML 문서 빌더 라이브러리"""

    def __init__(self, base_xml_path: str):
        """
        초기화
        Args:
            base_xml_path: 기본 XML 파일 경로 (section0.xml과 같은)
        """
        if base_xml_path:
            self.tree = ET.parse(base_xml_path)
            self.root = self.tree.getroot()
        else:
            # 기본 구조 생성
            self.root = self._create_base_structure()
            self.tree = ET.ElementTree(self.root)

    def _create_base_structure(self):
        """기본 HWP XML 구조 생성"""
        # 네임스페이스 정의
        namespaces = {
            'hs': 'http://www.hancom.co.kr/hwpml/2011/section',
            'hp': 'http://www.hancom.co.kr/hwpml/2011/paragraph',
            'hc': 'http://www.hancom.co.kr/hwpml/2011/core',
            'ha': 'http://www.hancom.co.kr/hwpml/2011/app',
            'hp10': 'http://www.hancom.co.kr/hwpml/2016/paragraph',
            'hh': 'http://www.hancom.co.kr/hwpml/2011/head',
            'hhs': 'http://www.hancom.co.kr/hwpml/2011/history',
            'hm': 'http://www.hancom.co.kr/hwpml/2011/master-page',
            'hpf': 'http://www.hancom.co.kr/schema/2011/hpf',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'opf': 'http://www.idpf.org/2007/opf/',
            'ooxmlchart': 'http://www.hancom.co.kr/hwpml/2016/ooxmlchart',
            'hwpunitchar': 'http://www.hancom.co.kr/hwpml/2016/HwpUnitChar',
            'epub': 'http://www.idpf.org/2007/ops',
            'config': 'urn:oasis:names:tc:opendocument:xmlns:config:1.0'
        }

        # 루트 요소 생성
        root = ET.Element('{http://www.hancom.co.kr/hwpml/2011/section}sec')

        # 네임스페이스 설정
        for prefix, uri in namespaces.items():
            root.set(f'xmlns:{prefix}', uri)

        return root

    def add_para_number_text(self, text: str, level: int = 1, style: str = "1") -> None:
        """
        제목 추가 (예: "실행파일", "HDEV-001")

        Args:
            text: 제목 텍스트
            level: 제목 레벨 (1: 주제목, 2: 부제목)
            style_id: 스타일 ID
        """
        # 고유 ID 생성
        para_id = str(abs(hash(text + str(level))))

        # 단락 요소 생성
        p_elem = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}p')
        p_elem.set('id', para_id)
        p_elem.set('paraPrIDRef', str(11 + 2 * level))
        p_elem.set('styleIDRef', style)
        p_elem.set('pageBreak', '0')
        p_elem.set('columnBreak', '0')
        p_elem.set('merged', '0')

        # 실행 요소 생성
        run_elem = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}run')
        run_elem.set('charPrIDRef', '2')

        # 텍스트 요소 생성
        text_elem = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}t')
        text_elem.text = text
        run_elem.append(text_elem)

        # 라인 세그먼트 배열 생성
        lineseg_array = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}linesegarray')
        lineseg = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}lineseg')
        lineseg.set('textpos', '0')
        lineseg.set('vertpos', '0')
        lineseg.set('vertsize', '1100')
        lineseg.set('textheight', '1100')
        lineseg.set('baseline', '935')
        lineseg.set('spacing', '660')
        lineseg.set('horzpos', '0')
        lineseg.set('horzsize', '43936')
        lineseg.set('flags', '2490368')

        lineseg_array.append(lineseg)
        p_elem.append(run_elem)
        p_elem.append(lineseg_array)

        self.root.append(p_elem)

    def add_text(self, text: str, para_pr_id: str = "13", style_id: str = "2") -> None:
        """
        문장 추가 (예: "○ HDEV-001의 실행파일 총 수 : 9")

        Args:
            text: 텍스트
            para_pr_id: 단락 속성 ID
            style_id: 스타일 ID
        """
        # 고유 ID 생성
        para_id = str(abs(hash(text)))

        # 단락 요소 생성
        p_elem = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}p')
        p_elem.set('id', para_id)
        p_elem.set('paraPrIDRef', para_pr_id)
        p_elem.set('styleIDRef', style_id)
        p_elem.set('pageBreak', '0')
        p_elem.set('columnBreak', '0')
        p_elem.set('merged', '0')

        # 실행 요소 생성
        run_elem = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}run')
        run_elem.set('charPrIDRef', '3')

        # 텍스트 요소 생성
        text_elem = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}t')
        text_elem.text = text
        run_elem.append(text_elem)

        # 라인 세그먼트 배열 생성
        lineseg_array = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}linesegarray')
        lineseg = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}lineseg')
        lineseg.set('textpos', '0')
        lineseg.set('vertpos', '0')
        lineseg.set('vertsize', '1100')
        lineseg.set('textheight', '1100')
        lineseg.set('baseline', '935')
        lineseg.set('spacing', '660')
        lineseg.set('horzpos', '0')
        lineseg.set('horzsize', '43936')
        lineseg.set('flags', '393216')

        lineseg_array.append(lineseg)
        p_elem.append(run_elem)
        p_elem.append(lineseg_array)

        self.root.append(p_elem)

    def add_table(self,
                  table_data: List[List[str]],
                  headers: List[str],
                  sizes: List[int],
                  caption: str = "표",
                  table_num: int = 1,
                  caption_suffix: str = "목록") -> None:
        """
        테이블 추가

        Args:
            table_data: 테이블 데이터 (2차원 리스트)
            headers: 헤더 리스트
            caption: 테이블 캡션 접두사
            table_num: 테이블 번호
            caption_suffix: 캡션 접미사
        """
        # 테이블 ID 생성
        table_id = str(abs(hash(caption + str(table_num))))

        # 빈 단락 추가
        self.add_empty_paragraph()

        # 테이블을 포함하는 단락 생성
        p_elem = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}p')
        p_elem.set('id', '0')
        p_elem.set('paraPrIDRef', '6')
        p_elem.set('styleIDRef', '0')
        p_elem.set('pageBreak', '0')
        p_elem.set('columnBreak', '0')
        p_elem.set('merged', '0')

        # 실행 요소 생성
        run_elem = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}run')
        run_elem.set('charPrIDRef', '36')

        # 테이블 요소 생성
        tbl_elem = self._create_table_element(
            table_data, headers, sizes, caption, table_num, caption_suffix, table_id)
        run_elem.append(tbl_elem)

        # 빈 텍스트 요소 추가
        text_elem = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}t')
        run_elem.append(text_elem)

        # 라인 세그먼트 배열 생성
        lineseg_array = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}linesegarray')
        lineseg = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}lineseg')
        lineseg.set('textpos', '0')
        lineseg.set('vertpos', '0')
        lineseg.set('vertsize', '1100')
        lineseg.set('textheight', '1100')
        lineseg.set('baseline', '935')
        lineseg.set('spacing', '660')
        lineseg.set('horzpos', '0')
        lineseg.set('horzsize', '0')
        lineseg.set('flags', '393216')

        lineseg_array.append(lineseg)
        p_elem.append(run_elem)
        p_elem.append(lineseg_array)

        self.root.append(p_elem)

    def _create_table_element(self,
                              table_data, headers: list[str], sizes: list[int],
                              caption: str, table_num: int, caption_suffix: str,
                              table_id: str):
        """테이블 요소 생성"""
        tbl = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}tbl')
        tbl.set('id', table_id)
        tbl.set('zOrder', '0')
        tbl.set('numberingType', 'TABLE')
        tbl.set('textWrap', 'TOP_AND_BOTTOM')
        tbl.set('textFlow', 'BOTH_SIDES')
        tbl.set('lock', '0')
        tbl.set('dropcapstyle', 'None')
        tbl.set('pageBreak', 'CELL')
        tbl.set('repeatHeader', '1')
        tbl.set('rowCnt', str(len(table_data) + 1))  # 헤더 + 저장위치 행들 포함
        tbl.set('colCnt', str(len(headers)))
        tbl.set('cellSpacing', '0')
        tbl.set('borderFillIDRef', '5')
        tbl.set('noAdjust', '0')

        # 테이블 크기 설정
        sz_elem = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}sz')
        sz_elem.set('width', '43534')
        sz_elem.set('widthRelTo', 'ABSOLUTE')
        sz_elem.set('height', '57300')
        sz_elem.set('heightRelTo', 'ABSOLUTE')
        sz_elem.set('protect', '0')
        tbl.append(sz_elem)

        # 위치 설정
        pos_elem = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}pos')
        pos_elem.set('treatAsChar', '0')
        pos_elem.set('affectLSpacing', '0')
        pos_elem.set('flowWithText', '1')
        pos_elem.set('allowOverlap', '0')
        pos_elem.set('holdAnchorAndSO', '0')
        pos_elem.set('vertRelTo', 'PARA')
        pos_elem.set('horzRelTo', 'COLUMN')
        pos_elem.set('vertAlign', 'TOP')
        pos_elem.set('horzAlign', 'LEFT')
        pos_elem.set('vertOffset', '0')
        pos_elem.set('horzOffset', '0')
        tbl.append(pos_elem)

        # 외부 여백 설정
        out_margin = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}outMargin')
        out_margin.set('left', '283')
        out_margin.set('right', '283')
        out_margin.set('top', '283')
        out_margin.set('bottom', '283')
        tbl.append(out_margin)

        # 캡션 설정
        caption_elem = self._create_caption_element(
            caption, table_num, caption_suffix)
        tbl.append(caption_elem)

        # 내부 여백 설정
        in_margin = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}inMargin')
        in_margin.set('left', '481')
        in_margin.set('right', '481')
        in_margin.set('top', '0')
        in_margin.set('bottom', '0')
        tbl.append(in_margin)

        # 헤더 행 생성
        header_row = self._create_header_row(headers, sizes)
        tbl.append(header_row)

        # 데이터 행들 생성
        self._add_table_data_rows(tbl, table_data, sizes, len(headers))

        return tbl

    def _create_caption_element(self, caption, table_num, caption_suffix):
        """캡션 요소 생성"""
        caption_elem = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}caption')
        caption_elem.set('side', 'TOP')
        caption_elem.set('fullSz', '0')
        caption_elem.set('width', '8504')
        caption_elem.set('gap', '850')
        caption_elem.set('lastWidth', '43534')

        # 서브리스트 생성
        sublist = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}subList')
        sublist.set('id', '')
        sublist.set('textDirection', 'HORIZONTAL')
        sublist.set('lineWrap', 'BREAK')
        sublist.set('vertAlign', 'TOP')
        sublist.set('linkListIDRef', '0')
        sublist.set('linkListNextIDRef', '0')
        sublist.set('textWidth', '0')
        sublist.set('textHeight', '0')
        sublist.set('hasTextRef', '0')
        sublist.set('hasNumRef', '0')

        # 캡션 단락 생성
        p = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}p')
        p.set('id', '0')
        p.set('paraPrIDRef', '1')
        p.set('styleIDRef', '3')
        p.set('pageBreak', '0')
        p.set('columnBreak', '0')
        p.set('merged', '0')

        # 실행 요소
        run = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}run')
        run.set('charPrIDRef', '2')

        # 캡션 텍스트
        t1 = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}t')
        t1.text = f"{caption} "
        run.append(t1)

        # 자동 번호
        ctrl = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}ctrl')
        autonum = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}autoNum')
        autonum.set('num', str(table_num))
        autonum.set('numType', 'TABLE')

        autonum_format = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}autoNumFormat')
        autonum_format.set('type', 'DIGIT')
        autonum_format.set('userChar', '')
        autonum_format.set('prefixChar', '')
        autonum_format.set('suffixChar', '')
        autonum_format.set('supscript', '0')

        autonum.append(autonum_format)
        ctrl.append(autonum)
        run.append(ctrl)

        # 접미사 텍스트
        t2 = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}t')
        t2.text = f" {caption_suffix}"
        run.append(t2)

        # 라인 세그먼트
        lineseg_array = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}linesegarray')
        lineseg = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}lineseg')
        lineseg.set('textpos', '0')
        lineseg.set('vertpos', '0')
        lineseg.set('vertsize', '1100')
        lineseg.set('textheight', '1100')
        lineseg.set('baseline', '935')
        lineseg.set('spacing', '660')
        lineseg.set('horzpos', '0')
        lineseg.set('horzsize', '43532')
        lineseg.set('flags', '393216')

        lineseg_array.append(lineseg)
        p.append(run)
        p.append(lineseg_array)
        sublist.append(p)
        caption_elem.append(sublist)

        return caption_elem

    def _create_header_row(self, headers: list[str], sizes: list[int]):
        """헤더 행 생성"""
        tr = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}tr')
        ends_col: int = len(headers) - 1
        for i, header in enumerate(headers):
            tc = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}tc')
            tc.set('name', '')
            tc.set('header', '1' if i == 0 else '0')
            tc.set('hasMargin', '1')
            tc.set('protect', '0')
            tc.set('editable', '0')
            tc.set('dirty', '0')
            if i != 0 and i != ends_col:
                tc.set('borderFillIDRef', '8')
            elif i == 0:
                tc.set('borderFillIDRef', '7')
            else:
                tc.set('borderFillIDRef', '9')

            # 서브리스트
            sublist = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}subList')
            sublist.set('id', '')
            sublist.set('textDirection', 'HORIZONTAL')
            sublist.set('lineWrap', 'BREAK')
            sublist.set('vertAlign', 'CENTER')
            sublist.set('linkListIDRef', '0')
            sublist.set('linkListNextIDRef', '0')
            sublist.set('textWidth', '0')
            sublist.set('textHeight', '0')
            sublist.set('hasTextRef', '0')
            sublist.set('hasNumRef', '0')

            # 단락
            p = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}p')
            p.set('id', '0')
            p.set('paraPrIDRef', '20')
            p.set('styleIDRef', '4')
            p.set('pageBreak', '0')
            p.set('columnBreak', '0')
            p.set('merged', '0')

            # 실행
            run = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}run')
            run.set('charPrIDRef', '1')

            # 텍스트
            t = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}t')
            t.text = header
            run.append(t)

            # 라인 세그먼트
            lineseg_array = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}linesegarray')
            lineseg = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}lineseg')
            lineseg.set('textpos', '0')
            lineseg.set('vertpos', '0')
            lineseg.set('vertsize', '1000')
            lineseg.set('textheight', '1000')
            lineseg.set('baseline', '850')
            lineseg.set('spacing', '500')
            lineseg.set('horzpos', '0')
            lineseg.set('horzsize', '3516')
            lineseg.set('flags', '393216')

            lineseg_array.append(lineseg)
            p.append(run)
            p.append(lineseg_array)
            sublist.append(p)
            tc.append(sublist)

            # 셀 주소
            cell_addr = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellAddr')
            cell_addr.set('colAddr', str(i))
            cell_addr.set('rowAddr', '0')
            tc.append(cell_addr)

            # 셀 스팬
            cell_span = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellSpan')
            cell_span.set('colSpan', '1')
            cell_span.set('rowSpan', '1')
            tc.append(cell_span)

            # 셀 크기
            cell_sz = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellSz')
            cell_sz.set('width', str(sizes[i]))
            cell_sz.set('height', '2275')
            tc.append(cell_sz)

            # 셀 여백
            cell_margin = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellMargin')
            cell_margin.set('left', '481')
            cell_margin.set('right', '481')
            cell_margin.set('top', '0')
            cell_margin.set('bottom', '0')
            tc.append(cell_margin)

            tr.append(tc)

        return tr

    def _add_table_data_rows(self, tbl_elem, table_data: List[List[str]], sizes: list[int], col_count: int):
        """
        테이블에 데이터 행들을 추가

        Args:
            tbl_elem: 테이블 요소
            table_data: 테이블 데이터 (2차원 리스트)
            col_count: 컬럼 수
        """
        row_index = 1  # 헤더 다음부터 시작
        row_length = len(table_data)
        for row_data in table_data:
            if row_data[0].startswith("저장위치:"):
                storage_row = self._create_storage_location_row(
                    row_data[0], col_count, row_index)
                tbl_elem.append(storage_row)
            else:
                # 일반 데이터 행 추가
                data_row = self._create_data_row(
                    row_data, sizes, row_index, col_count, row_length == row_index)
                tbl_elem.append(data_row)

            row_index += 1

    def _create_storage_location_row(self, location_text: str, col_count: int, row_index: int):
        """
        저장위치 행 생성 (전체 컬럼 스팬)

        Args:
            location_text: 저장위치 텍스트
            col_count: 전체 컬럼 수
            row_index: 행 인덱스
        """
        tr = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}tr')

        # 단일 셀로 전체 컬럼 스팬
        tc = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}tc')
        tc.set('name', '')
        tc.set('header', '0')
        tc.set('hasMargin', '0')
        tc.set('protect', '0')
        tc.set('editable', '0')
        tc.set('dirty', '0')
        tc.set('borderFillIDRef', '10')

        # 서브리스트
        sublist = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}subList')
        sublist.set('id', '')
        sublist.set('textDirection', 'HORIZONTAL')
        sublist.set('lineWrap', 'BREAK')
        sublist.set('vertAlign', 'CENTER')
        sublist.set('linkListIDRef', '0')
        sublist.set('linkListNextIDRef', '0')
        sublist.set('textWidth', '0')
        sublist.set('textHeight', '0')
        sublist.set('hasTextRef', '0')
        sublist.set('hasNumRef', '0')

        # 단락
        p = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}p')
        p.set('id', '0')
        p.set('paraPrIDRef', '4')
        p.set('styleIDRef', '6')
        p.set('pageBreak', '0')
        p.set('columnBreak', '0')
        p.set('merged', '0')

        # 실행
        run = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}run')
        run.set('charPrIDRef', '0')

        # 텍스트
        t = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}t')
        t.text = location_text
        run.append(t)

        # 라인 세그먼트
        lineseg_array = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}linesegarray')
        lineseg = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}lineseg')
        lineseg.set('textpos', '0')
        lineseg.set('vertpos', '0')
        lineseg.set('vertsize', '1000')
        lineseg.set('textheight', '1000')
        lineseg.set('baseline', '850')
        lineseg.set('spacing', '500')
        lineseg.set('horzpos', '0')
        lineseg.set('horzsize', '42572')
        lineseg.set('flags', '1441792')

        lineseg_array.append(lineseg)
        p.append(run)
        p.append(lineseg_array)
        sublist.append(p)
        tc.append(sublist)

        # 셀 주소
        cell_addr = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellAddr')
        cell_addr.set('colAddr', '0')
        cell_addr.set('rowAddr', str(row_index))
        tc.append(cell_addr)

        # 셀 스팬 (전체 컬럼 스팬)
        cell_span = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellSpan')
        cell_span.set('colSpan', str(col_count))
        cell_span.set('rowSpan', '1')
        tc.append(cell_span)

        # 셀 크기
        cell_sz = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellSz')
        cell_sz.set('width', '43534')
        cell_sz.set('height', '2275')
        tc.append(cell_sz)

        # 셀 여백
        cell_margin = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellMargin')
        cell_margin.set('left', '510')
        cell_margin.set('right', '510')
        cell_margin.set('top', '141')
        cell_margin.set('bottom', '141')
        tc.append(cell_margin)

        tr.append(tc)
        return tr

    def _create_data_row(self, row_data: List[str], sizes: list[int], row_index: int, col_count: int, ends: bool = False):
        """
        일반 데이터 행 생성

        Args:
            row_data: 행 데이터 리스트
            row_index: 행 인덱스
            col_count: 컬럼 수
        """
        tr = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}tr')

        # 행 데이터가 컬럼 수보다 적으면 빈 값으로 채움
        padded_data = row_data + [''] * (col_count - len(row_data))

        for col_index, cell_data in enumerate(padded_data[:col_count]):
            tc = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}tc')
            tc.set('name', '')
            tc.set('header', '0')
            tc.set('hasMargin', '0')
            tc.set('protect', '0')
            tc.set('editable', '0')
            tc.set('dirty', '0')

            if ends is False:
                if col_index == 0:
                    border_fill_id = '14'
                elif col_index == col_count - 1:
                    border_fill_id = '15'
                else:
                    border_fill_id = '5'
            else:
                if col_index == 0:
                    border_fill_id = '16'
                elif col_index == col_count - 1:
                    border_fill_id = '17'
                else:
                    border_fill_id = '11'

            tc.set('borderFillIDRef', border_fill_id)

            # 서브리스트
            sublist = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}subList')
            sublist.set('id', '')
            sublist.set('textDirection', 'HORIZONTAL')
            sublist.set('lineWrap', 'BREAK')
            sublist.set('vertAlign', 'CENTER')
            sublist.set('linkListIDRef', '0')
            sublist.set('linkListNextIDRef', '0')
            sublist.set('textWidth', '0')
            sublist.set('textHeight', '0')
            sublist.set('hasTextRef', '0')
            sublist.set('hasNumRef', '0')

            # 단락
            p = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}p')
            p.set('id', '0')
            if col_index == col_count - 1:
                p.set('paraPrIDRef', '4')
                p.set('styleIDRef', '6')
            else:
                p.set('paraPrIDRef', '6')
                p.set('styleIDRef', '5')
            p.set('pageBreak', '0')
            p.set('columnBreak', '0')
            p.set('merged', '0')

            # 실행
            run = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}run')
            run.set('charPrIDRef', '0')

            # 텍스트
            t = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}t')
            t.text = str(cell_data) if cell_data else ''
            run.append(t)

            # 라인 세그먼트 생성
            lineseg_array = self._create_cell_lineseg(
                cell_data, sizes[col_index], col_index)

            p.append(run)
            p.append(lineseg_array)
            sublist.append(p)
            tc.append(sublist)

            # 셀 주소
            cell_addr = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellAddr')
            cell_addr.set('colAddr', str(col_index))
            cell_addr.set('rowAddr', str(row_index))
            tc.append(cell_addr)

            # 셀 스팬
            cell_span = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellSpan')
            cell_span.set('colSpan', '1')
            cell_span.set('rowSpan', '1')
            tc.append(cell_span)

            # 셀 크기 (컬럼에 따라 다른 크기)
            cell_sz = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellSz')

            width = str(sizes[col_index])
            cell_sz.set('width', width)
            cell_sz.set('height', '2275')
            tc.append(cell_sz)

            # 셀 여백
            cell_margin = ET.Element(
                '{http://www.hancom.co.kr/hwpml/2011/paragraph}cellMargin')
            cell_margin.set('left', '0')
            cell_margin.set('right', '0')
            cell_margin.set('top', '0')
            cell_margin.set('bottom', '0')
            tc.append(cell_margin)

            tr.append(tc)

        return tr

    def _create_cell_lineseg(self, cell_data: str, size: int, col_index: int):
        """
        셀의 라인 세그먼트 생성 (긴 텍스트의 경우 여러 줄 처리)

        Args:
            cell_data: 셀 데이터
            col_index: 컬럼 인덱스
        """
        lineseg_array = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}linesegarray')

        # 일반적인 단일 라인 세그먼트
        lineseg = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}lineseg')
        lineseg.set('textpos', '0')
        lineseg.set('vertpos', '0')
        lineseg.set('vertsize', '1000')
        lineseg.set('textheight', '1000')
        lineseg.set('baseline', '850')
        lineseg.set('spacing', '500')
        lineseg.set('horzpos', '0')

        # 컬럼별 크기 설정
        horzsize = str(size - 992)
        lineseg.set('horzsize', horzsize)
        lineseg.set('flags', '1441792')

        lineseg_array.append(lineseg)

        return lineseg_array

    def add_empty_paragraph(self):
        """빈 단락 추가"""
        p_elem = ET.Element('{http://www.hancom.co.kr/hwpml/2011/paragraph}p')
        p_elem.set('id', '0')
        p_elem.set('paraPrIDRef', '13')
        p_elem.set('styleIDRef', '2')
        p_elem.set('pageBreak', '0')
        p_elem.set('columnBreak', '0')
        p_elem.set('merged', '0')

        run_elem = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}run')
        run_elem.set('charPrIDRef', '3')

        lineseg_array = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}linesegarray')
        lineseg = ET.Element(
            '{http://www.hancom.co.kr/hwpml/2011/paragraph}lineseg')
        lineseg.set('textpos', '0')
        lineseg.set('vertpos', '0')
        lineseg.set('vertsize', '1100')
        lineseg.set('textheight', '1100')
        lineseg.set('baseline', '935')
        lineseg.set('spacing', '660')
        lineseg.set('horzpos', '0')
        lineseg.set('horzsize', '43936')
        lineseg.set('flags', '393216')

        lineseg_array.append(lineseg)
        p_elem.append(run_elem)
        p_elem.append(lineseg_array)

        self.root.append(p_elem)

    def save(self, output_path: str):
        """XML 파일로 저장"""
        # XML 선언과 네임스페이스 처리
        ET.register_namespace(
            'hs', 'http://www.hancom.co.kr/hwpml/2011/section')
        ET.register_namespace(
            'hp', 'http://www.hancom.co.kr/hwpml/2011/paragraph')
        ET.register_namespace('hc', 'http://www.hancom.co.kr/hwpml/2011/core')

        self.tree.write(output_path, encoding='UTF-8', xml_declaration=True)
