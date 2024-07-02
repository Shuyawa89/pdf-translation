# pdf_processing.py

import pdf2image
import numpy as np

DPI = 72

def pdf_to_image(file_path, page_num):
    """
    PDFファイルを画像に変換する関数

    @param file_path: PDFファイルのパス
    @param page_num: 変換するページ番号
    @return: 画像としてのページ
    """
    return np.asarray(pdf2image.convert_from_path(file_path, dpi=DPI)[page_num])

def is_inside(paragraph_block, text_block):
    """
    特定のtext_blockがparagraph_blockに含まれているかチェックする関数

    @param paragraph_block: 段落ブロック
    @param text_block: テキストブロック
    @return: 含まれている場合はTrue、それ以外はFalse
    """
    paragraph_width = paragraph_block.block.x_2 - paragraph_block.block.x_1
    paragraph_height = paragraph_block.block.y_2 - paragraph_block.block.y_1
    if paragraph_width > 300:
        allowable_error_pixel = 10
        return (text_block.block.x_1 >= paragraph_block.block.x_1 - allowable_error_pixel and
                text_block.block.x_2 <= paragraph_block.block.x_2 + allowable_error_pixel and
                text_block.block.y_1 >= paragraph_block.block.y_1 - allowable_error_pixel and
                text_block.block.y_2 <= paragraph_block.block.y_2 + allowable_error_pixel)
    return False
