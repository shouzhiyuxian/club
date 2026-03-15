# -*- coding: utf-8 -*-
"""Excel 导出工具：将 QuerySet 或列表导出为 xlsx"""
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
import datetime


def export_to_excel(rows, headers, filename="export.xlsx", sheet_name="Sheet1"):
    """
    导出为 Excel 文件。
    :param rows: 二维列表或元组，每行一行数据（与 headers 顺序一致）
    :param headers: 表头列表
    :param filename: 下载文件名（不含路径）
    :param sheet_name: 工作表名称
    :return: HttpResponse
    """
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name[:31]  # Excel 表名最多 31 字符
    
    # 表头
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    # 数据行
    for row_idx, row_data in enumerate(rows, 2):
        for col_idx, value in enumerate(row_data, 1):
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M") if value else ""
            elif isinstance(value, datetime.date):
                value = value.strftime("%Y-%m-%d") if value else ""
            ws.cell(row=row_idx, column=col_idx, value=value)
    
    # 列宽（粗略按表头长度）
    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 14
    
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response
