import io
from reportlab.platypus import Paragraph, KeepInFrame
from reportlab.platypus.frames import Frame
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfWriter, PdfReader

from pdf_processing import pdf_to_image, is_inside, fill_cover, calc_fontsize, get_max_font_size
from translation import translate_text
import layoutparser as lp

if __name__ == "__main__":
    DPI = 72

    # フォントの登録
    font_name = 'BIZUDGothic'
    font_ttf = 'BIZUDGothic-Regular.ttf'
    pdfmetrics.registerFont(TTFont(font_name, font_ttf))

    # ファイルパスの入力を受け付ける
    target_pdf_file_path = r"./Improvement of CT Reconstruction Using Scattered X-Rays.pdf"

    is_mihiraki = True

    # PDFの基本情報を取得
    base_pdf = PdfReader(open(target_pdf_file_path, "rb"))
    _, _, base_width, base_height = base_pdf.pages[0].mediabox

    output = PdfWriter()

    # レイアウトモデルのロード
    model = lp.Detectron2LayoutModel(
        config_path='lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
        model_path='/root/.torch/iopath_cache/s/57zjbwv6gh3srry/model_final.pth',
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
        label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
    )

    pdf_pages, _ = lp.load_pdf(target_pdf_file_path, load_images=True, dpi=DPI)

    for page_index, pdf_page in enumerate(pdf_pages):
        print(f"■{page_index} ページ目")
        text_blocks = pdf_page.get_homogeneous_blocks()
        pdf_image = pdf_to_image(target_pdf_file_path, page_index)
        height, width, channel = pdf_image.shape
        print(height, width)
        plt.imshow(pdf_image)
        pdf_layout = model.detect(pdf_image)
        paragraph_blocks = lp.Layout([b for b in pdf_layout if b.type == 'Text'])

        cover_packet = io.BytesIO()
        cover_canvas = canvas.Canvas(cover_packet, pagesize=(int(base_width), int(base_height)), bottomup=True)

        text_packet = io.BytesIO()
        text_canvas = canvas.Canvas(text_packet, pagesize=(int(base_width), int(base_height)), bottomup=True)

        for paragraph_block in paragraph_blocks:
            inner_text_blocks = list(filter(lambda x: is_inside(paragraph_block, x), text_blocks))
            print(len(inner_text_blocks))
            if len(inner_text_blocks) == 0:
                continue

            text = " ".join(list(map(lambda x: x.text, inner_text_blocks)))
            print(text)
            translated_text = translate_text(text)
            print(translated_text)

            paragraph_x = (paragraph_block.block.x_1 / width) * base_width
            paragraph_y = (paragraph_block.block.y_2 / height) * base_height
            paragraph_width = ((paragraph_block.block.x_2 - paragraph_block.block.x_1) / width) * base_width
            paragraph_height = ((paragraph_block.block.y_2 - paragraph_block.block.y_1) / height) * base_height

            fill_cover(cover_canvas, paragraph_x, height - paragraph_y, paragraph_width, paragraph_height)

            frame = Frame(paragraph_x, height - paragraph_y, paragraph_width, paragraph_height, showBoundary=0, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
            fontsize = calc_fontsize(paragraph_width, paragraph_height, translated_text)
            style = ParagraphStyle(name='Normal', fontName=font_name, fontSize=fontsize, leading=fontsize)
            paragraph = Paragraph(translated_text, style)
            story = [paragraph]
            story_inframe = KeepInFrame(paragraph_width * 1.5, paragraph_height * 1.5, story)
            frame.addFromList([story_inframe], text_canvas)

        cover_canvas.save()
        cover_packet.seek(0)
        cover_pdf = PdfReader(cover_packet)
        text_canvas.save()
        text_packet.seek(0)
        text_pdf = PdfReader(text_packet)

        base_pdf = PdfReader(open(target_pdf_file_path, "rb"))
        base_page = base_pdf.pages[page_index]
        if is_mihiraki:
            output.add_page(base_page)
        try:
            base_page.merge_page(cover_pdf.pages[0])
            base_page.merge_page(text_pdf.pages[0])
        except Exception as e:
            print(f"error: {e}")

        output.add_page(base_page)

    output_filepath = "translated_" + target_pdf_file_path.split('/')[-1]
    print(output_filepath)
    with open(output_filepath, "wb") as outputStream:
        output.write(outputStream)

    print(f"翻訳済みPDFが {output_filepath} に保存されました。")
