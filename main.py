import sys
from config import FileTranslator
from pdf_translator import PdfTranslator
from parsing import ParseArgs


def main() -> None:
    """Main function"""
    arguments: ParseArgs = ParseArgs(sys.argv)

    translate_file: FileTranslator = None
    if arguments.filetype == ".pdf":
        translate_file = PdfTranslator(arguments.translator)

    translate_file.translate(arguments.dst_path, arguments.src_path)


if __name__ == "__main__":
    main()
