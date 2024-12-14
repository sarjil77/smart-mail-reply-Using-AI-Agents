import imaplib
import email
from email.header import decode_header
import os
import boto3
import json
import uuid
import tempfile
from pdf2image import convert_from_path
from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

email_user = "xyz@gmail.com"
email_pass = "958 bolt a champion"

# your code for ocr client will go here


# Paths
attachment_save_path = "/data/aiuserinj/sarjil/mail_summarizer/handling_attachments"

# Initialize IMAP client
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# Initialize AWS Textract client
textract_client = boto3.client('textract', 
                               aws_access_key_id=aws_access_key_id, 
                               aws_secret_access_key=aws_secret_access_key, 
                               region_name='us-east-1')

def login():
    print("Logging in...")
    imap.login(email_user, email_pass)
    print("Logged in.")

def logout():
    print("Logging out...")
    imap.close()
    imap.logout()
    print("Logged out.")

def fetch_unseen_emails():
    print("Fetching unseen emails...")
    imap.select("inbox")
    status, messages = imap.search(None, '(UNSEEN)')
    print(f"Unseen emails fetched: {messages[0].split()}")
    return messages[0].split()

def extract_text_from_image(image_path):
    print(f"Extracting text from image: {image_path}")
    with open(image_path, 'rb') as img_file:
        response = textract_client.detect_document_text(Document={'Bytes': img_file.read()})
        text = ""
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text += block['Text'] + "\n"
    print(f"Extracted text from image: {text[:100]}...")  # Print the first 100 characters for brevity
    return text

def extract_text_from_pdf_as_images(pdf_path):
    print(f"Extracting text from PDF as images: {pdf_path}")
    text = ""
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(pdf_path, output_folder=path)
        for i, image in enumerate(images):
            image_path = os.path.join(path, f"page_{i}.jpg")
            image.save(image_path, 'JPEG')
            text += extract_text_from_image(image_path)
    print(f"Extracted text from PDF: {text[:100]}...")  # Print the first 100 characters for brevity
    return text

def save_attachment(part, filename):
    print(f"Saving attachment: {filename}")
    filepath = os.path.join(attachment_save_path, filename)
    with open(filepath, "wb") as f:
        f.write(part.get_payload(decode=True))
    print(f"Attachment saved at: {filepath}")
    return filepath

def process_email_with_attachments():
    print("Processing emails with attachments...")
    messages = fetch_unseen_emails()
    for mail in messages:
        _, msg = imap.fetch(mail, "(RFC822)")
        for response_part in msg:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = decode_header(msg["subject"])[0][0]
                email_from = decode_header(msg["from"])[0][0]
                print(f"Processing email - Subject: {email_subject}, From: {email_from}")

                email_content = ""
                ocr_content = ""
                image_files = []
                pdf_files = []

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_disposition() == "attachment":
                            filename = part.get_filename()
                            if filename:
                                filepath = save_attachment(part, filename)
                                if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                                    image_files.append(filepath)
                                elif filename.lower().endswith(".pdf"):
                                    pdf_files.append(filepath)
                        else:
                            # Extract text from non-attachment parts of the email
                            try:
                                email_content += part.get_payload(decode=True).decode()
                            except:
                                pass  # Skip if decoding fails
                else:
                    # Single part email, extract content directly
                    email_content = msg.get_payload(decode=True).decode()

                # Process image files
                print(f"Image files to process: {image_files}")
                for image_file in image_files:
                    ocr_content += extract_text_from_image(image_file)
                
                # Process PDFs
                if pdf_files:
                    print(f"PDF files to process: {pdf_files}")
                    for pdf_file in pdf_files:
                        ocr_content += extract_text_from_pdf_as_images(pdf_file)

                # Define AI agents
                print("Defining AI agents...")
                model = Ollama(model="llama3.1:8b")
                classifier = create_classifier_agent(model)
                summarizer = summarizer_of_ocr(model)
                
                # Define tasks
                print("Defining tasks...")
                classify_email_task = Task(
                    description=f'classify the email content: {email_content}',
                    agent=classifier,
                    expected_output="one of the three outputs: 'important', 'casual', 'spam'",
                    output_format="json"
                )

                summarize_ocr_task = Task(
                    description=f'summarize the OCR content: {ocr_content}',
                    agent=summarizer,
                    expected_output="a concise summary of the important details from the OCR content",
                     output_format="json"
                )

                # Create and run the crew
                print("Creating and running the crew...")
                crew = Crew(
                    agents=[classifier, summarizer],
                    tasks=[classify_email_task, summarize_ocr_task],
                    verbose=0,
                    full_output=True,
                    process=Process.sequential
                )
                result = crew.kickoff()
                print("Crew run completed.")

                # Extract and save outputs
                classify_email_output = classify_email_task.output.json()
                summarize_ocr_output = summarize_ocr_task.output.json()
                print(f"Classifier output: {classify_email_output}")
                print(f"Summarizer output: {summarize_ocr_output}")

                try:
                    classify_email_output_decoded = json.loads(classify_email_output)
                except json.JSONDecodeError:
                    classify_email_output_decoded = classify_email_output

                try:
                    summarize_ocr_output_decoded = json.loads(summarize_ocr_output)
                except json.JSONDecodeError:
                    summarize_ocr_output_decoded = summarize_ocr_output

                # Generate a unique ID for this email
                email_id = str(uuid.uuid4())

                # Append the results with unique ID
                email_result = {
                    "ID": email_id,
                    "From": email_from,
                    "Subject": email_subject,
                    "Content": email_content,
                    "Classifier Output": classify_email_output_decoded,
                    "Summarizer Output": summarize_ocr_output_decoded
                }

                # Save results to JSON file
                output_filepath = '/data/aiuserinj/sarjil/mail_summarizer/handling_attachments/task_output_of_email&attch.json'
                try:
                    with open(output_filepath, 'w') as json_file:
                        json.dump(email_result, json_file, indent=4)
                    logging.info(f"Results saved to {output_filepath}")
                except Exception as e:
                    logging.error(f"Failed to save results to {output_filepath}. Error: {str(e)}")

def create_classifier_agent(model):
    """Creates and returns a classifier agent."""
    print("Creating classifier agent...")
    return Agent(
        role='email classifier',
        goal='accurately classify emails. Give one of these ratings: important, casual, spam',
        backstory='You are an AI assistant whose only job is to classify emails accurately and give a bad rating if the content of the mail is bad',
        verbose=False,
        allow_delegation=False,
        llm=model
    )

def summarizer_of_ocr(model):
    """Creates and returns a summary of an OCR."""
    print("Creating summarizer agent...")
    return Agent(
        role='OCR summarizer',
        goal='Extract and summarize important details from OCR content. Identify the type of attachment and key points.',
        backstory='You are an AI assistant specializing in processing OCR content. Your task is to read the provided OCR text, understand its context, and summarize the key points concisely. Ensure to capture the type of attachment and the most important details.',
        verbose=False,
        allow_delegation=False,
        llm=model,
        max_iter=30
    )

def main():
    login()
    try:
        process_email_with_attachments()
    finally:
        logout()

if __name__ == "__main__":
    main()
