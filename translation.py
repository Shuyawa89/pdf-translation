from transformers import pipeline

translator = pipeline('translation', model='staka/fugumt-en-ja')

def translate_text(text):
    """
    英語のテキストを日本語に翻訳する。

    @param text: 翻訳したい英語のテキスト
    @return: 翻訳された日本語のテキスト
    """
    translated_text = ""
    if len(text) > 1000:
        n = len(text)
        i1 = n // 3
        i2 = i1 * 2
        text1 = text[:i1]
        text2 = text[i1:i2]
        text3 = text[i2:]
        result1 = translator(text1)
        result2 = translator(text2)
        result3 = translator(text3)
        translated_text = result1[0]['translation_text'] + result2[0]['translation_text'] + result3[0]['translation_text']
    else:
        result = translator(text)
        translated_text = result[0]['translation_text']
    return translated_text
