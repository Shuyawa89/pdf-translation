import json
import google.generativeai as genai
import os
import time
import re

# env.jsonからAPIキーを読み込み
with open('env.json', 'r') as f:
    env = json.load(f)

genai.configure(api_key=env['GEMINI_API_KEY'])

model = genai.GenerativeModel(model_name='gemini-1.5-flash')
chat = model.start_chat()

api_call_count = 0  # API呼び出し回数をカウントする変数

def translate_text_gemini(text):
    """
    英語のテキストを日本語に翻訳する。

    @param text: 翻訳したい英語のテキスト
    @return: 翻訳された日本語のテキスト
    """
    global api_call_count
    api_call_count += 1
    print("連続呼び出しを防ぐために15秒待機します。")
    time.sleep(15)
    print(f"API呼び出し回数: {api_call_count}回目")
    
    separator = "\n---\n"  # 区切り文字
    prompt = f"Translate the following English text to Japanese. Include the separator '{separator}' between each translated block. Return only the translated text.\n\n{text}"
    response = chat.send_message(prompt)
    translated_text = response.text.strip()

    # HTMLタグを除去
    translated_text = re.sub(r'<[^>]+>', '', translated_text)
    return translated_text

def split_translated_text(translated_text, separator="\n---\n"):
    """
    翻訳された日本語のテキストを区切り文字で分割する。

    @param translated_text: 区切り文字を含む翻訳された日本語のテキスト
    @param separator: 区切り文字
    @return: 分割された翻訳された日本語のテキストのリスト
    """
    return translated_text.split(separator)
