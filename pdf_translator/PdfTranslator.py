import fitz
from fitz import Rect
from fitz import Pixmap
from fitz import open as open_pdf
from fitz import Document, Page
from config import FileTranslator

TEXT_BLOCK: int = 0
IMAGE_BLOCK: int = 1


class PdfTranslator(FileTranslator):
    """Translate pdf files"""

    @staticmethod
    def safe_insert_textbox(page: Page, rect: Rect, text: str, fontname: str,
                            fontsize: int, align: int, scales: list) -> bool:
        if not fontname.lower().startswith(("helv", "times", "cour")):
            fontname = "helv"
        for scale in scales:
            result: int = page.insert_textbox(
                rect,
                text,
                fontname=fontname,
                fontsize=fontsize * scale,
                align=align
            )
            if result >= 0:
                return True
        return False

    def translate_text_block(self, dst_page: Page, text_block: dict) -> None:
        for line in text_block["lines"]:
            for span in line["spans"]:
                x0, y0, x1, y1 = span["bbox"]
                text: str = span["text"]
                fontname: str = span["font"]
                fontsize: int = span["size"]
                if not text.strip():
                    continue
                translated_text: str = self._FileTranslator__translator(text)
                self.safe_insert_textbox(
                    dst_page,
                    Rect(x0, y0, x1, y1),
                    translated_text,
                    fontname,
                    fontsize,
                    fitz.TEXT_ALIGN_LEFT,
                    [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
                )

    @staticmethod
    def copy_image_block(dst_page: Page, src_page: Page,
                         image_block: dict) -> None:
        img_rect: Rect = Rect(image_block["bbox"])
        pixmap: Pixmap = src_page.get_pixmap(clip=img_rect)
        dst_page.insert_image(img_rect, pixmap=pixmap)

    def translate_page(self, dst_page: Page, src_page: Page) -> None:
        blocks: dict = src_page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == TEXT_BLOCK:
                self.translate_text_block(dst_page, block)
            else:
                self.copy_image_block(dst_page, src_page, block)

    def translate(self, dst_path: str, src_path: str) -> None:
        src_pdf: Document = open_pdf(src_path)
        dst_pdf: Document = open_pdf()
        for i, page in enumerate(src_pdf):
            new_page: Page = dst_pdf.new_page(
                width=page.rect.width,
                height=page.rect.height
            )
            self.translate_page(new_page, page)
            print(f"Done {i + 1} pages translated from {src_pdf.page_count}")
        dst_pdf.save(dst_path)
