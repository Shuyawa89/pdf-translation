from transformers import pipeline
import torch
import re

device = 0 if torch.cuda.is_available() else -1  # GPUが使用可能な場合は0、そうでない場合は-1

# translator = pipeline("translation", model="staka/fugumt-en-ja", device=device) # このモデルはなぜか文章がバグる
model = "Hoax0930/marian-finetuned-kde4-en-to-ja_kftt"
translator = pipeline("translation", model=model, device=device)

def translate_text(text, num_splits=3):
    """
    英語のテキストを日本語に翻訳する。

    @param text: 翻訳したい英語のテキスト
    @param num_splits: テキストを分割する数
    @return: 翻訳された日本語のテキスト
    """

    def split_text(text, num_splits):
        """テキストを指定した数に分割する。分割点は最も近い句読点で区切る。"""
        length = len(text)
        approx_len = length // num_splits
        splits = []
        start = 0
        for i in range(1, num_splits):
            split_point = start + approx_len
            if split_point < length:
                # 次の句読点を探す
                next_punctuation = max(text.rfind('.', start, split_point),
                                       text.rfind('!', start, split_point),
                                       text.rfind('?', start, split_point))
                if next_punctuation != -1:
                    split_point = next_punctuation + 1
                else:
                    split_point = start + approx_len  # 句読点が見つからない場合はそのまま分割
            splits.append(text[start:split_point].strip())
            start = split_point
        splits.append(text[start:].strip())  # 残りのテキストを追加
        return splits
    
    def remove_extra_spaces(text):
        """テキスト中の不要な空白を取り除く。"""
        text = re.sub(r'\s+', ' ', text)  # 連続する空白を一つの空白に置換
        text = re.sub(r'(\S) (\S)', r'\1\2', text)  # 単語間の空白を除去
        text = re.sub(r'(\S) (\S)', r'\1\2', text)  # 単語間の空白を除去

        return text

    translated_text = ""
    if len(text) > 250:
        split_texts = split_text(text, num_splits)
        translated_parts = [translator(part)[0]['translation_text'] for part in split_texts]
        translated_text = ''.join(translated_parts)
    else:
        result = translator(text)
        translated_text = result[0]['translation_text']
    
    # HTMLタグを除去
    translated_text = re.sub(r'<[^>]+>', '', translated_text)
    # 不要な空白を取り除く
    translated_text = remove_extra_spaces(translated_text)
    
    return translated_text
