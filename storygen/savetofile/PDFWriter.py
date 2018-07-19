import pypdflite


class PDFWriter:

    def main(self):
        writer = pypdflite.PDFLite("hello.pdf")
        writer.set_information(title="Hello World!")
        document = writer.get_document()
        document.add_text("Hello World!")
        writer.close()

if  __name__ == '__main__':
    PDFWriter().main()
