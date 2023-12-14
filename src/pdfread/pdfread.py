import click
import subprocess
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
# import io

# Path to the Tesseract executable (update this path based on your installation)
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

total_text = ""


def extract_text_from_image(image_path):
    global total_text
    try:
        # Open the image file
        image = Image.open(image_path)

        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(image)

        # Print the extracted text
        # print("Extracted Text:\n", text)
        total_text = total_text + text
    except Exception as e:
        print(f"Error: {e}")


def extract_text_from_pdf(pdf_path):
    global total_text
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Iterate through all the pages in the PDF
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            # Extract normal text from the page
            pdf_text = page.get_text()
            # print(f"Extracted Text from Page {page_number + 1}:\n", pdf_text)
            total_text = total_text + pdf_text
            # Check if there are images on the page

            # Extract images from the page and perform OCR
            images = page.get_images(full=True)
            if images:
                for img_index, img_info in enumerate(images, start=1):
                    xref = img_info[0]  # get the XREF of the image
                    pix = fitz.Pixmap(pdf_document, xref)  # create a Pixmap

                    if pix.n - pix.alpha > 3:  # CMYK: convert to RGB first
                        pix = fitz.Pixmap(fitz.csRGB, pix)

                    pix.save("/tmp/temp.png")  # save the image as png
                    pix = None

                    # Use pytesseract to do OCR on the image
                    extract_text_from_image("/tmp/temp.png")

    except Exception as e:
        print(f"Error: {e}")

@click.group()
@click.version_option('0.1.1', prog_name='PDFread')
def main():
    '''pdfread is the CLI pdf reader that builds itself on OCR technology to work on both scanned and typed PDFs.'''
    pass

@main.command("read", help="Read a PDF File")
@click.argument("file", nargs=1)
def read(file):
    extract_text_from_pdf(file)
    with open ("/tmp/temp.txt", "w") as f:
        f.write(total_text)
        f.close()
    subprocess.run(f"vim /tmp/temp.txt", shell=True)


if __name__=="__main__":
    main()