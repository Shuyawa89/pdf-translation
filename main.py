# main.py

import os
from pdf_processing import pdf_to_image, is_inside
from utils import download_font

def main():
    # 初期設定
    input_pdf_path = r"C:\Users\shu\OneDrive - 筑波大学\M2\参考論文\E104.D_2020EDP7241.pdf"

    is_mihiraki = True

    # フォントをダウンロード
    font_name = 'BIZUDGothic'
    font_ttf = 'BIZUDGothic-Regular.ttf'
    font_url = f'https://github.com/googlefonts/morisawa-biz-ud-gothic/raw/main/fonts/ttf/{font_ttf}'
    download_font(font_url, font_ttf)

    # PDFの画像変換テスト
    page_num = 0  # テスト用に最初のページを使用
    image = pdf_to_image(pdf_file_path, page_num)
    print(f'Page {page_num} of the PDF converted to image successfully.')

if __name__ == '__main__':
    main()

