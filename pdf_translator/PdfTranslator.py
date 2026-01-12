import fitz
from fitz import open as open_pdf
from fitz import Document, Page
from typing import Optional
from config import FileTranslator


class PdfTranslator(FileTranslator):
    """Translate pdf files"""

    def translate_page(self, dst_page: Page, src_page: Page) -> None:
        blocks: tuple = src_page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    x0, y0, x1, y1 = span["bbox"]
                    text: str = span["text"]
                    fontname: str = span["font"]
                    fontsize: int = span["size"]
                    if not text.strip():
                        continue
                    translated_text: str = self.__translator(text)
                    dst_page.insert_textbox(
                        fitz.Rect(x0, y0, x1, y1),
                        translated_text,
                        fontname=fontname,
                        fontsize=fontsize,
                        align=fitz.TEXT_ALIGN_LEFT
                    )

    def translate(self, dst_path: str, src_path: str) -> None:
        src_pdf: Document = open_pdf(src_path)
        dst_pdf: Document = open_pdf()
        for page in src_pdf:
            new_page: Page = dst_pdf.new_page(
                width=page.rect.width,
                height=page.rect.height
            )
            self.translate_page(new_page, page)
        dst_pdf.save(dst_path)
