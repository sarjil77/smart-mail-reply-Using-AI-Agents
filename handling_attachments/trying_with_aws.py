import boto3
import os
import tempfile
from pdf2image import convert_from_path

# your ocr credentials should be here


# Initialize AWS Textract client
textract_client = boto3.client(
    'textract',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

def extract_text_from_image(image_path):
    """Extract text from a single image file using AWS Textract."""
    with open(image_path, 'rb') as image_file:
        response = textract_client.detect_document_text(Document={'Bytes': image_file.read()})
        text = ""
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text += block['Text'] + "\n"
    return text

# def extract_text_from_pdf(pdf_path):
    """Convert PDF to images and extract text from each image using AWS Textract."""
    text = ""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert PDF to images
        images = convert_from_path(pdf_path, output_folder=temp_dir)
        for image in images:
            image_path = os.path.join(temp_dir, f"page_{images.index(image)}.jpg")
            image.save(image_path, 'JPEG')
            text += extract_text_from_image(image_path)
    return text

def main():
    # Paths to image and PDF files
    image_path = '/data/aiuserinj/sarjil/mail_summarizer/handling_attachments/coverages_ex.jpg'
    # pdf_path = 'path/to/your/document.pdf'

    # Extract text from image
    print(f"Extracting text from image: {image_path}")
    image_text = extract_text_from_image(image_path)
    print("Extracted text from image:")
    print(image_text)

    # Extract text from PDF
    # print(f"Extracting text from PDF: {pdf_path}")
    # pdf_text = extract_text_from_pdf(pdf_path)
    # print("Extracted text from PDF:")
    # print(pdf_text)

if __name__ == "__main__":
    main()
