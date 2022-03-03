# Pdf info:
# https://realpython.com/pdf-python/

from PyPDF2 import PdfFileReader        # type: ignore


def pdf_numpages(pdf_path: str) -> int:
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        return pdf.getNumPages()
