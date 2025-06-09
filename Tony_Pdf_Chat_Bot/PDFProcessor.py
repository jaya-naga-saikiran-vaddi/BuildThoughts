from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFProcessor:
    def __init__(self, file):
        self.file = file
        self.text = ""
        self.chunks = []

    def extractText(self):
        pdf_reader = PdfReader(self.file)
        if len(pdf_reader.pages) == 0:
            raise ValueError("The uploaded PDF is empty or invalid.")
        for page in pdf_reader.pages:
            self.text += page.extract_text() or ""

    def splitText(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.chunks = text_splitter.split_text(self.text)