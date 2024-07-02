# utils.py

import urllib.request

def download_font(font_url, font_ttf):
    """
    フォントをダウンロードする関数

    @param font_url: フォントのURL
    @param font_ttf: 保存するフォントファイル名
    """
    urllib.request.urlretrieve(font_url, font_ttf)
    print(f'Font {font_ttf} downloaded successfully.')
