import PyPDF2
import sys


def get_text_from_pdf(path_to_pdf_file):
    pdf_file_object = open(path_to_pdf_file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_object)

    page_object = pdf_reader.getPage(0)
    text = page_object.extractText()
    print(text.encode('utf-8'))


if __name__ == '__main__':
    print(sys.argv[1])
    get_text_from_pdf(sys.argv[1])
