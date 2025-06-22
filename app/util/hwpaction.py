import uuid
from typing import List, Literal
from pyhwpx import Hwp


class HwpAction:
    def __init__(self, hwp: Hwp) -> None:
        self.hwp = hwp
        self.para_level = 1

    def set_para_level_up(self) -> None:
        self.hwp.Run("ParaNumberBulletLevelUp")
        self.para_level -= 1

    def set_para_level_down(self) -> None:
        self.hwp.Run("ParaNumberBulletLevelDown")
        self.para_level += 1

    def set_para_number(self, level: int) -> None:
        self.hwp.Run("ParaNumberBulletLevelDown")
        while self.para_level != level:
            if self.para_level - level > 0:
                self.set_para_level_up()
            else:
                self.set_para_level_down()

    def set_para_number_text(self, text: str, level: int, style: str) -> None:
        self.set_para_number(level)
        self.set_style(style)
        self.insert_text(text)
        self.BreakPara()
        self.BreakPara()
        self.set_style("바탕글")

    def set_style_with_text(self, text: str, style: str) -> None:
        self.set_style(style)
        self.insert_text(text)
        self.BreakPara()

    def set_column_cell_text(self, text: str) -> None:
        self.hwp.ParagraphShapeAlignCenter()
        self.insert_text(text)
        self.set_style("05_도표내용_항목제목")
        self.hwp.cell_fill((214, 214, 214))

    def set_column_cel_border(self,
                              left: bool, top: bool,
                              right: bool, bottom: bool) -> None:
        self.hwp.TableCellBlock()
        boder = self.hwp.HParameterSet.HCellBorderFill
        if left:
            boder.BorderWidthLeft = 6
        if right:
            boder.BorderWidthRight = 6
        if top:
            boder.BorderWidthTop = 6
        if bottom:
            boder.BorderWidthBottom = 6
        self.hwp.HAction.Execute("CellBorderFill", boder.HSet)

    def set_table_columns(self, columns: List[str], width: List[float]) -> None:
        for index, cols in enumerate(columns):
            self.set_column_cell_text(cols)
            if index == 0:
                self.set_column_cel_border(True, True, False, True)
            elif index == len(columns) - 1:
                self.set_column_cel_border(False, True, True, True)
            else:
                self.set_column_cel_border(False, True, False, True)
            self.set_col_width(width[index])
            self.hwp.set_cell_margin(1.7, 1.7, 0, 0)
            self.TableRightCell()
        self.hwp.Run("Cancel")

    def set_table_border(self,
                         left: bool, top: bool,
                         right: bool, bottom: bool) -> None:
        self.hwp.TableCellBlock()
        self.hwp.TableCellBlockExtend()
        self.hwp.TableCellBlockExtend()

        boder = self.hwp.HParameterSet.HCellBorderFill
        if left:
            boder.BorderWidthLeft = 6
        if right:
            boder.BorderWidthRight = 6
        if top:
            boder.BorderWidthTop = 6
        if bottom:
            boder.BorderWidthBottom = 6
        self.hwp.HAction.Execute("CellBorderFill", boder.HSet)
        self.hwp.Run("Cancel")

    def set_caption(self,
                    text: str,
                    location: Literal["Top", "Bottom",
                                      "Left", "Right"] = "Top",
                    align: Literal[
                        "Left", "Center", "Right", "Distribute", "Division", "Justify"
                    ] = "Center",) -> None:
        self.hwp.ShapeObjAttachCaption()
        self.set_style("04_도표그림_제목")
        self.insert_text(text)

        if align == "Left":
            self.hwp.ParagraphShapeAlignLeft()
        elif align == "Center":
            self.hwp.ParagraphShapeAlignCenter()
        elif align == "Right":
            self.hwp.ParagraphShapeAlignRight()
        elif align == "Distribute":
            self.hwp.ParagraphShapeAlignDistribute()
        elif align == "Division":
            self.hwp.ParagraphShapeAlignDivision()
        elif align == "Justify":
            self.hwp.ParagraphShapeAlignJustify()

        param = self.hwp.HParameterSet.HShapeObject
        self.hwp.HAction.GetDefault("TablePropertyDialog", param.HSet)
        param.ShapeCaption.Side = self.hwp.SideType(location)
        self.hwp.HAction.Execute("TablePropertyDialog", param.HSet)
        self.hwp.CloseEx()

    def set_col_width(self, width: float) -> None:
        self.hwp.set_col_width(width, as_='mm')

    def merge_table_row(self) -> None:
        self.hwp.TableCellBlockExtendAbs()
        self.hwp.Run("TableColEnd")
        self.hwp.Run("TableMergeCell")
        self.hwp.Run("Cancel")

    def set_row(self, *rows: str) -> None:
        for row in rows:
            self.set_style("07_도표내용_본문혼합")
            self.insert_text(row)
            self.hwp.TableCellBlock()
            self.TableRightCell()
            self.hwp.Cancel()

    def save(self) -> str:
        file = self._random_filename()
        self.hwp.save_as(file)
        return file

    # dir(hwp.HParameterSet)

    def open(self, file: str) -> None:
        self.hwp.open(file)

    def create_table(self, rows: int, cols: int,
                     treat_as_char: bool, header: bool) -> None:
        self.hwp.create_table(rows=rows, cols=cols,
                              treat_as_char=treat_as_char, header=header)
        self.hwp.set_table_inside_margin(1.7, 1.7, 0, 0, as_='mm')

    def insert_text(self, text: str) -> None:
        self.hwp.insert_text(text)

    def set_style(self, style: str | int) -> None:
        self.hwp.set_style(style)

    def TableRightCell(self):
        self.hwp.TableRightCell()

    def TableCellBlock(self):
        self.hwp.TableCellBlock()

    def Cancel(self):
        self.hwp.Cancel()

    def BreakPara(self):
        self.hwp.BreakPara()

    def _random_filename(self):
        return str(uuid.uuid4())+".hwp"
