import os
import json
import uuid
import tempfile
from pdf2image import convert_from_path
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from ai_agents import create_classifier_agent, create_image_summarizer_agent, create_pdf_summarizer_agent, create_email_responder
import logging
import boto3

# your code for OCR client would go here


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths
attachment_save_path = "/data/aiuserinj/sarjil/mail_summarizer/handling_attachments"
json_filepath = '/data/aiuserinj/sarjil/mail_summarizer/final_email_with_ocr_and_text/unseen_emails_info.json'

def extract_text_from_image(image_path):
    logging.info(f"Extracting text from image: {image_path}")
    with open(image_path, 'rb') as img_file:
        response = textract_client.detect_document_text(Document={'Bytes': img_file.read()})
        text = "".join([block['Text'] + "\n" for block in response['Blocks'] if block['BlockType'] == 'LINE'])
    logging.info(f"Extracted text from image: {text[:100]}...")
    return text

def extract_text_from_pdf_as_images(pdf_path):
    logging.info(f"Extracting text from PDF as images: {pdf_path}")
    text = ""
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(pdf_path, output_folder=path)
        for i, image in enumerate(images):
            image_path = os.path.join(path, f"page_{i}.jpg")
            image.save(image_path, 'JPEG')
            text += extract_text_from_image(image_path)
    logging.info(f"Extracted text from PDF: {text[:100]}...")
    return text

def process_emails_from_json():
    logging.info("Processing emails from JSON...")

    # Load the JSON data
    with open(json_filepath, 'r') as json_file:
        emails = json.load(json_file)

    # List to hold results of all emails
    all_email_results = []

    # Iterate over each email
    for email_data in emails:
        email_subject = email_data["Subject"]
        email_from = email_data["From"]
        email_received = email_data["Date"]
        email_content = email_data["Content"]
        attachments = email_data["Attachments"]

        logging.info(f"Processing email - Subject: {email_subject}, From: {email_from}, Received: {email_received}")

        # Separate attachments by type
        image_files = [att['Path'] for att in attachments if att['Filename'].lower().endswith((".jpg", ".jpeg", ".png"))]
        pdf_files = [att['Path'] for att in attachments if att['Filename'].lower().endswith(".pdf")]

        # Handle no attachments case
        if not image_files and not pdf_files:
            logging.info(f"No attachments found for email: {email_subject}")
            continue

        # Define AI agents
        model = Ollama(model="llama3.1:8b")
        classifier = create_classifier_agent(model)
        responder = create_email_responder(model)
        image_summarizer = create_image_summarizer_agent(model)
        pdf_summarizer = create_pdf_summarizer_agent(model)

        # Process image files
        image_ocr_results = []
        for image_file in image_files:
            ocr_content = extract_text_from_image(image_file)
            classify_image_task = Task(
                description=f'Summarize the OCR content from the image: {ocr_content}',
                agent=image_summarizer,
                expected_output='A concise summary of the OCR content...',
            )
            crew_image = Crew(agents=[image_summarizer], tasks=[classify_image_task], process=Process.sequential)
            crew_image.kickoff()
            summarize_image_output = classify_image_task.output.raw
            image_ocr_results.append({
                "Image File": image_file,
                "Summary": summarize_image_output
            })

        # Process PDF files
        pdf_ocr_results = []
        for pdf_file in pdf_files:
            ocr_content = extract_text_from_pdf_as_images(pdf_file)
            classify_pdf_task = Task(
                description=f'Summarize the content of the PDF document: {ocr_content}',
                agent=pdf_summarizer,
                expected_output='A concise summary of the PDF content...',
            )
            crew_pdf = Crew(agents=[pdf_summarizer], tasks=[classify_pdf_task], process=Process.sequential)
            crew_pdf.kickoff()
            summarize_pdf_output = classify_pdf_task.output.raw
            pdf_ocr_results.append({
                "PDF File": pdf_file,
                "Summary": summarize_pdf_output
            })

        # Define and run the classifier task
        classify_email_task = Task(
            description=f'Classify the email content: {email_content}',
            agent=classifier,
            expected_output="one of the following categories: 'Policy Inquiries', ...",
        )
        crew_classifier = Crew(agents=[classifier], tasks=[classify_email_task], process=Process.sequential)
        crew_classifier.kickoff()
        classify_email_output = classify_email_task.output.raw

        # Define and run the responder task
        responder_email_task = Task(
            description=f'Respond to the email content: {email_content}',
            agent=responder,
            expected_output="A very concise response...",
        )
        crew_responder = Crew(agents=[responder], tasks=[responder_email_task], process=Process.sequential)
        crew_responder.kickoff()
        responder_email_output = responder_email_task.output.raw

        # Generate a unique ID for this email
        email_id = str(uuid.uuid4())

        # Append the results with unique ID
        email_result = {
            "ID": email_id,
            "From": email_from,
            "Subject": email_subject,
            "Received": email_received,
            "Content": email_content,
            "Classifier Output": classify_email_output,
            "Responder Output": responder_email_output,
            "Attachments": {
                "Images": image_ocr_results,
                "PDFs": pdf_ocr_results
            }
        }

        # Append the result to the list
        all_email_results.append(email_result)

    # Save all results to a single JSON file
    output_filepath = '/data/aiuserinj/sarjil/mail_summarizer/final_email_with_ocr_and_text/all_email_results_aug_18.json'
    logging.info(f'Saving all results to: {output_filepath}')
    try:
        with open(output_filepath, 'w') as json_file:
            json.dump(all_email_results, json_file, indent=4)
        logging.info(f"All results saved to {output_filepath}")
    except Exception as e:
        logging.error(f"Failed to save all results to {output_filepath}. Error: {str(e)}")

if __name__ == "__main__":
    process_emails_from_json()
