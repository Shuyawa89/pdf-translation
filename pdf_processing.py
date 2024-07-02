import pdf2image
import numpy as np
import matplotlib.pyplot as plt

DPI = 72

def pdf_to_image(file_path, page_num):
    """
    PDFファイルの特定ページを画像として読み込む。

    @param file_path: PDFファイルのパス
    @param page_num: 読み込みたいページ番号
    @return: 読み込んだ画像をNumPy配列として返す
    """
    return np.asarray(pdf2image.convert_from_path(file_path, dpi=DPI)[page_num])

def is_inside(paragraph_block, text_block):
    """
    特定のtext_blockがparagraph_blockに含まれているかをチェックする。

    @param paragraph_block: 段落ブロック
    @param text_block: テキストブロック
    @return: テキストブロックが段落ブロックに含まれている場合はTrue、それ以外はFalse
    """
    paragraph_width = paragraph_block.block.x_2 - paragraph_block.block.x_1
    paragraph_height = paragraph_block.block.y_2 - paragraph_block.block.y_1
    allowable_error_pixel = 10 if paragraph_width > 300 else 3
    return (text_block.block.x_1 >= paragraph_block.block.x_1 - allowable_error_pixel and 
            text_block.block.y_1 >= paragraph_block.block.y_1 and
            text_block.block.x_2 <= paragraph_block.block.x_2 + allowable_error_pixel and 
            text_block.block.y_2 <= paragraph_block.block.y_2 + allowable_error_pixel)

def fill_cover(canvas, x, y, width, height):
    """
    段落ブロックを塗りつぶすカバーを描画する。

    @param canvas: 描画対象のキャンバス
    @param x: カバーの左上のX座標
    @param y: カバーの左上のY座標
    @param width: カバーの幅
    @param height: カバーの高さ
    """
    canvas.setFillColorRGB(1, 1, 1)
    canvas.rect(x - 5 if width > 300 else x, y, width + 10 if width > 300 else width, height + 10 if width > 300 else height, stroke=0, fill=1)

def calc_fontsize(paragraph_width, paragraph_height, translated_text):
    """
    段落の幅と高さ、および翻訳されたテキストから適切なフォントサイズを計算する。

    @param paragraph_width: 段落の幅
    @param paragraph_height: 段落の高さ
    @param translated_text: 翻訳されたテキスト
    @return: 計算されたフォントサイズ
    """
    return int(np.sqrt(paragraph_width * paragraph_height / len(translated_text)))

def get_max_font_size(paragraph_width, paragraph_height, translated_text, font_face="./BIZUDGothic-Regular.ttf", max_font_size=100):
    """
    指定された領域内で最大のフォントサイズを求める。

    @param paragraph_width: 段落の幅
    @param paragraph_height: 段落の高さ
    @param translated_text: 翻訳されたテキスト
    @param font_face: 使用するフォントファイルのパス
    @param max_font_size: 最大フォントサイズ（デフォルトは100）
    @return: 適切なフォントサイズ
    """
    from PIL import ImageFont
    for font_size in range(max_font_size, 0, -1):
        font = ImageFont.truetype(font_face, font_size)
        text_width, text_height = font.getsize(translated_text)
        if text_width <= paragraph_width and text_height <= paragraph_height:
            return font_size
    return 0
